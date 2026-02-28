import uuid
import json
import os
import re
from pathlib import Path
from typing import Dict, Optional

import aiofiles
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from orchestrator.types import ITRRunResult, TaxpayerProfile, TaxRegime, IncomeComponents, DeductionComponents
from orchestrator.graph import run_itr_workflow, resume_itr_workflow
from document_parser import extract_text_from_file
from pydantic import BaseModel
from db import init_db, save_run, load_run, load_all_runs

# ─── App setup ───────────────────────────────────────────────────────────────

app = FastAPI(
    title="Agentic ITR Auto-Filer API",
    description="Automatically extract, compute, and file ITR-1 from Form 16 + Bank Interest Statement",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB on startup
@app.on_event("startup")
def startup_event():
    init_db()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


# ─── Health ───────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "service": "Agentic ITR Auto-Filer", "version": "1.0.0"}


# ─── Debug: Extract text from uploaded file ─────────────────────────────────

@app.post("/itr/debug-extract")
async def debug_extract_text(
    file: UploadFile = File(...),
):
    """Debug endpoint: Upload a file and see extracted text."""
    from pathlib import Path
    import tempfile
    
    # Save temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        # Extract text
        raw_text = extract_text_from_file(tmp_path, file.content_type)
        
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "extracted_text_length": len(raw_text),
            "extracted_text_preview": raw_text[:2000],  # First 2000 chars
            "full_text": raw_text  # Send full text so user can see it
        }
    finally:
        Path(tmp_path).unlink()  # Clean up


# ─── Upload documents (MAIN ENTRY POINT) ──────────────────────────────────────

@app.post("/itr/upload")
async def upload_and_run(
    files: list[UploadFile] = File(...),
    name: str = Form(default="Taxpayer"),
    pan: str = Form(default="ABCDE1234F"),
    age: int = Form(default=30),
    regime: str = Form(default="OLD"),
):
    """
    🚀 MAIN ENTRY POINT: Upload Form 16 and/or Bank Interest Statement
    
    The system will:
    1. Extract text from each document (OCR if needed)
    2. Classify documents (Form 16 vs Bank Statement)
    3. Extract structured fields (salary, income, TDS, deductions)
    4. Aggregate income from all sources
    5. Validate deductions and apply caps
    6. Compute tax liability using slabs
    7. Select appropriate ITR form (ITR-1 for salaried)
    8. Fill ITR form with extracted data
    9. E-verify the return
    
    Returns complete ITR filing with refund/payable amount and agent timeline.
    """
    run_id = str(uuid.uuid4())
    run_upload_dir = UPLOAD_DIR / run_id
    run_upload_dir.mkdir(parents=True, exist_ok=True)
    
    docs_raw = []
    
    for file in files:
        # Save file
        file_path = run_upload_dir / file.filename
        async with aiofiles.open(file_path, "wb") as f:
            content = await file.read()
            await f.write(content)
        
        # Extract text
        try:
            raw_text = extract_text_from_file(str(file_path), file.content_type)
        except Exception as e:
            from document_parser import OCRDependencyError
            # Fail explicitly if extraction fails - don't silently use hardcoded mock data
            if isinstance(e, OCRDependencyError):
                raise HTTPException(
                    status_code=422,
                    detail=f"PDF extraction failed: {str(e)}. This appears to be a scanned image-based PDF. "
                           f"Please install Tesseract OCR or provide a text-based PDF. "
                           f"Error details: {e}"
                )
            else:
                raise HTTPException(
                    status_code=422,
                    detail=f"Failed to extract text from '{file.filename}': {str(e)}"
                )
    
        entry = {
            "filename": file.filename,
            "raw_text": raw_text,
        }
        docs_raw.append(entry)
    
    taxpayer = TaxpayerProfile(
        name=name,
        pan=pan,
        age=age,
        regime=TaxRegime(regime.upper()),
    )
    
    try:
        result = run_itr_workflow(docs_raw=docs_raw)
        result.run_id = run_id
        result.taxpayer = taxpayer
        # Ensure JSON-serializable for DB and response
        run_dict = result.model_dump(mode="json")
        save_run(result.run_id, result.created_at, run_dict)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ─── List all runs ────────────────────────────────────────────────────────────

@app.get("/itr/runs")
def list_runs():
    """List all past ITR filing runs (most recent first)."""
    runs_list = []
    for run_dict in load_all_runs():
        # Quick fallback mapping if parsing fails
        try:
            r = ITRRunResult(**run_dict)
            runs_list.append({
                "run_id": r.run_id,
                "created_at": r.created_at,
                "taxpayer_name": r.taxpayer.name,
                "pan": r.taxpayer.pan,
                "financial_year": r.taxpayer.financial_year,
                "status": r.filing_status.status.value,
                "net_refund": r.tax_computation.net_refund,
                "net_payable": r.tax_computation.net_payable,
                "total_income": r.aggregated_income.gross_total_income,
            })
        except Exception as e:
            print(f"Error parsing run from DB: {e}")
            
    return runs_list


# ─── Get single run ───────────────────────────────────────────────────────────

@app.get("/itr/runs/{run_id}", response_model=ITRRunResult)
def get_run(run_id: str):
    """Get the full result for a specific ITR run."""
    run_dict = load_run(run_id)
    if not run_dict:
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found")
    return ITRRunResult(**run_dict)


# ─── Resume run ───────────────────────────────────────────────────────────────

class ResumeInput(BaseModel):
    income: IncomeComponents
    deduction_components: DeductionComponents

@app.post("/itr/runs/{run_id}/resume", response_model=ITRRunResult)
def resume_run(run_id: str, payload: ResumeInput):
    run_dict = load_run(run_id)
    if not run_dict:
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found")
        
    old_run = ITRRunResult(**run_dict)
    
    if old_run.filing_status.status != "NEEDS_REVIEW":
        raise HTTPException(status_code=400, detail="Only runs in NEEDS_REVIEW status can be resumed.")
        
    try:
        new_run = resume_itr_workflow(old_run, payload.income, payload.deduction_components)
        save_run(new_run.run_id, new_run.created_at, new_run.model_dump())
        return new_run
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ─── Get timeline steps ───────────────────────────────────────────────────────

@app.get("/itr/runs/{run_id}/steps")
def get_run_steps(run_id: str):
    """Get the agent timeline steps for a specific run."""
    run_dict = load_run(run_id)
    if not run_dict:
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found")
    
    r = ITRRunResult(**run_dict)
    return {"run_id": run_id, "steps": r.agent_steps}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
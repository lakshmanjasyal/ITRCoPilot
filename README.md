# Agentic ITR Auto-Filer 🤖🏛️

> India's first multi-agent AI copilot for Income Tax Return filing. Upload Form 16 → auto-extract → compute tax → e-verify ITR-1 in seconds.

## ✨ Features

- **8 AI Agents**: Document Classifier → Field Extractor → Income Aggregator → Deduction Claimer → Tax Computation → ITR Form Filler → E-Verifier → Supervisor
- **Form 16 OCR Parsing**: Upload PDF or image of Form 16, bank interest statement
- **Accurate Tax Computation**: Slab-wise computation for Old and New regime, Section 80C/80D deductions, Rebate 87A, HEC cess
- **ITR-1 JSON Preview**: Complete machine-readable ITR-1 with all schedules (A, S, OS, VIA)
- **E-Verification Simulation**: Mock Aadhaar OTP verification with acknowledgement number
- **Regime Comparison**: Side-by-side Old vs New regime tax comparison
- **Tax Optimization Tips**: Personalized suggestions to reduce tax liability
- **Agent Timeline**: Full audit trail showing each agent's work

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+

> **OCR Requirements:**
> - Install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and ensure the `tesseract` binary is on your system `PATH`. This is required for processing scanned Form 16/Bank PDFs.
> - (Optional but recommended) Install [Poppler](https://poppler.freedesktop.org/) (provides `pdftoppm`) to allow PDF‑to‑image conversion when Tesseract is used. On Windows you can add Poppler to PATH or place the binaries alongside the app.
> 
> Without these tools the backend will return a 400 error suggesting installation. For purely text-based PDFs, no additional dependencies are needed.

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Then open http://localhost:5173

## ⏱️ For Judges: 60-Second Live Demo

Already have Python environment ready? Here's the fastest path:

```bash
# Terminal 1: Start backend (FastAPI)
cd backend && uvicorn main:app --reload --port 8000

# Terminal 2: Start frontend (Vite)
cd frontend && npm run dev
# Browser automatically opens to http://localhost:5173
```

**Then in the UI:**
1. Click **"Run Demo Scenario"** (Rahul Sharma - ₹8.5L salary + ₹2L interest)
2. Watch the **18-step agent timeline** process the ITR
3. Click **"View Calculation Details"** to see tax breakdown
4. See **₹18,000 refund** and **ITR-1 form ready**

**Or upload your own:**
1. Click **"New Filing"** → Upload a Form 16 PDF/image
2. System auto-extracts: Salary, TDS, Interest, Deductions
3. Auto-computes tax in old & new regime
4. Shows side-by-side comparison + optimization tips

## 🎯 Demo Scenario

Click **"Run Demo Scenario"** to instantly see:
- **Rahul Sharma**: Salary ₹8,50,000 + FD Interest ₹2,00,000
- **Deductions**: 80C ₹1,50,000 + 80D ₹25,000
- **Result**: ITR-1 E-Verified ✅, **Refund ~₹18,000**

## 📁 Project Structure

```
agentic-itr-copilot/
├── backend/
│   ├── main.py                  # FastAPI app + all REST endpoints
│   ├── document_parser.py       # PDF/OCR text extraction
│   ├── orchestrator/
│   │   ├── types.py             # Pydantic models for all agents
│   │   └── graph.py             # All 8 agent implementations
│   ├── rules/
│   │   ├── slabs.json           # Tax slabs (Old + New regime)
│   │   └── deductions.json      # Section-wise deduction limits
│   └── samples/
│       ├── form16_rahul_sharma.txt
│       └── bank_interest_statement.txt
└── frontend/
    ├── src/
    │   ├── App.jsx              # Main app with state management
    │   ├── components/
    │   │   ├── RunsList.jsx     # Sidebar fills list
    │   │   ├── RunDetail.jsx    # Main detail view with tabs
    │   │   ├── TaxSummary.jsx   # Tax computation breakdown
    │   │   ├── FormPreview.jsx  # ITR-1 form preview
    │   │   ├── Timeline.jsx     # Agent processing timeline
    │   │   ├── TaxTips.jsx      # Optimization recommendations
    │   │   ├── NewRunModal.jsx  # Manual entry + file upload
    │   │   └── WelcomeScreen.jsx
    │   └── index.css            # Premium dark-mode design system
    └── index.html
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/itr/run` | File ITR from JSON input |
| POST | `/itr/upload` | File ITR from document upload (scanned PDFs require Tesseract/Poppler) |
| POST | `/itr/demo` | Run demo scenario (₹8.5L salary) |
| GET | `/itr/runs` | List all past runs |
| GET | `/itr/runs/{id}` | Get full run details |
| GET | `/itr/runs/{id}/steps` | Get agent timeline steps |

## 🤖 Agent Architecture

```
Upload/Input → [Supervisor Agent]
                    ↓
         [DocClassifierAgent] → classify FORM_16 / BANK_INT
                    ↓
         [FieldExtractionAgent] → regex/heuristic field extraction
                    ↓
       [IncomeAggregatorAgent] → sum all income heads
                    ↓
        [DeductionClaimerAgent] → apply limits (80C cap ₹1.5L, etc.)
                    ↓
        [TaxComputationAgent] → slab-wise + cess + rebate 87A
                    ↓
          [ITRFormFillerAgent] → map to ITR-1 schema
                    ↓
        [EVerificationAgent] → mock Aadhaar OTP e-verify
                    ↓
                 RESULT ✅
```

## 🏆 Hackathon Notes

Built for **Agentic AI Hackathon 2025** following best practices from:
- **Province** (AWS AI Agent Hackathon 3rd place): Robust document pipeline + ITR mapping
- **ITYaar** (Syrus 2025): OCR + AI tax computation + voice UI
- **SaveHaven**: RAG over tax rules for deduction explanations
- **Spend Guard**: Document AI + explainable decisions

**Key differentiators:**
1. True multi-agent orchestration with auditable step trail
2. Rule-based deduction capping (no hallucinations)
3. Old vs New regime comparison built-in
4. Real-time agent timeline for transparency

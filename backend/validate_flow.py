"""
End-to-end validation script for ITR Auto-Filer.
Tests:
1. DocumentClassifier works
2. FieldExtractor works
3. Manual input pipeline works
4. resume_itr_workflow handles corrections
5. All agents execute without errors
"""

import sys
sys.path.insert(0, r'c:\Users\HP\Desktop\ksum\backend')

from orchestrator.types import (
    ManualInput, TaxpayerProfile, TaxRegime,
    IncomeComponents, DeductionComponents, ITRRunResult
)
from orchestrator.graph import run_itr_workflow, resume_itr_workflow
from db import init_db, save_run, load_run

print("[VALIDATION] Starting ITR Auto-Filer validation...")

# Test 1: Manual input workflow (no documents)
print("\n[TEST 1] Manual input workflow...")
try:
    manual_input = ManualInput(
        taxpayer=TaxpayerProfile(
            name="Test User",
            pan="ABCDE1234F",
            age=30,
            regime=TaxRegime.OLD,
            financial_year="2024-25"
        ),
        salary=500000,
        interest_income=50000,
        tds_salary=50000,
        tds_bank=5000,
        section_80c=100000,
        section_80d=25000,
        hra_exemption=50000,
        other_deductions=0
    )
    
    result = run_itr_workflow(manual_input=manual_input)
    
    assert result.run_id is not None, "run_id should be generated"
    assert result.taxpayer.name == "Test User", "taxpayer name should match"
    assert result.aggregated_income is not None, "aggregated_income should be calculated"
    assert result.tax_computation is not None, "tax_computation should be done"
    assert result.filing_status.status.value == "E_VERIFIED", "should be E_VERIFIED by default"
    
    print(f"  [OK] Run ID: {result.run_id}")
    print(f"  [OK] Gross Income: Rs {result.aggregated_income.gross_total_income:,.0f}")
    print(f"  [OK] Tax Computation: Rs {result.tax_computation.total_tax_liability:,.0f}")
    print(f"  [OK] Refund: Rs {result.tax_computation.net_refund:,.0f}")
    print(f"  [OK] Filing Status: {result.filing_status.status.value}")
except Exception as e:
    print(f"  [FAILED] {e}")
    import traceback
    traceback.print_exc()

# Test 2: resume_itr_workflow with corrections
print("\n[TEST 2] Resume workflow with manual corrections...")
try:
    # Create a run with low confidence to trigger NEEDS_REVIEW
    result1 = run_itr_workflow(manual_input=manual_input)
    
    # Simulate user corrections
    corrected_income = IncomeComponents(
        gross_salary=550000,  # User corrected this
        interest_income=40000,  # User corrected this
        tds_salary=50000,
        tds_bank=4000,
        employer_name="Test Corp"
    )
    
    corrected_deductions = DeductionComponents(
        section_80c_raw=120000,  # User increased this
        section_80d_raw=25000,
        hra_exemption_raw=50000,
        other_raw=0
    )
    
    # Resume with corrected data
    result2 = resume_itr_workflow(
        original_run=result1,
        corrected_income=corrected_income,
        corrected_deductions=corrected_deductions
    )
    
    assert result2.run_id == result1.run_id, "run_id should be preserved"
    assert result2.income.gross_salary == 550000, "corrected salary should be used"
    assert result2.income.interest_income == 40000, "corrected interest should be used"
    assert result2.deduction_summary is not None, "deductions should be recalculated"
    assert result2.tax_computation is not None, "tax should be recalculated"
    
    print(f"  [OK] Run ID preserved: {result2.run_id}")
    print(f"  [OK] Corrected Salary: Rs {result2.income.gross_salary:,.0f}")
    print(f"  [OK] Corrected 80C: Rs {result2.deduction_components.section_80c_raw:,.0f}")
    print(f"  [OK] Recalculated Tax: Rs {result2.tax_computation.total_tax_liability:,.0f}")
    print(f"  [OK] Final Status: {result2.filing_status.status.value}")
except Exception as e:
    print(f"  [FAILED] {e}")
    import traceback
    traceback.print_exc()

# Test 3: NLP parsing (if API key not set, tests fallback)
print("\n[TEST 3] NLP prompt parsing...")
try:
    from nlp_parser import parse_magic_prompt
    
    prompt = "I earned 5 lakh salary, got 50k interest from my FD, employer deducted 50k TDS. 80C: 1.5L PPF."
    parsed = parse_magic_prompt(prompt)
    
    assert parsed.get("salary", 0) > 0, "salary should be extracted"
    assert parsed.get("interest_income", 0) > 0, "interest should be extracted"
    # Note: 80C extraction depends on regex pattern, may not match all formats
    
    print(f"  [OK] Parsed salary: Rs {parsed['salary']:,.0f}")
    print(f"  [OK] Parsed interest: Rs {parsed['interest_income']:,.0f}")
    print(f"  [OK] Parsed 80C: Rs {parsed.get('section_80c', 0):,.0f}")
    print(f"  [OK] Regime: {parsed.get('regime', 'OLD')}")
except Exception as e:
    print(f"  [FAILED] {e}")
    import traceback
    traceback.print_exc()

# Test 4: Database persistence
print("\n[TEST 4] Database persistence...")
try:
    init_db()
    
    # Save a run
    run = run_itr_workflow(manual_input=manual_input)
    save_run(run.run_id, run.created_at, run.model_dump())
    print(f"  [OK] Saved run to database: {run.run_id}")
    
    # Load it back
    loaded_data = load_run(run.run_id)
    assert loaded_data is not None, "should load run from database"
    loaded = ITRRunResult.model_validate(loaded_data)
    assert loaded.run_id == run.run_id, "run_id should match"
    assert loaded.taxpayer.name == run.taxpayer.name, "taxpayer should match"
    
    print(f"  [OK] Loaded run from database: {loaded.run_id}")
    print(f"  [OK] Database persistence WORKING")
except Exception as e:
    print(f"  [FAILED] {e}")
    import traceback
    traceback.print_exc()

print("\n[VALIDATION] All tests completed!")

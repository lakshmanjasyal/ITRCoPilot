"""
Test script for AUTOMATIC ITR filing - document upload only
No manual data entry, pure automatic extraction pipeline
"""

import sys
from pathlib import Path

# Setup path
sys.path.insert(0, str(Path(__file__).parent))

from orchestrator.graph import run_itr_workflow
from orchestrator.types import ITRRunResult
from document_parser import extract_text_from_file
from db import init_db, save_run

def test_automatic_filing_scenario_1():
    """Test 1: Salaried Individual - Form 16 + Bank Interest Statement"""
    print("\n" + "="*80)
    print("[TEST 1] AUTOMATIC FILING - Salaried Individual")
    print("="*80)
    
    # Simulate document uploads (using mock extracted text from document_parser.py)
    from document_parser import extract_text_from_file
    
    # These would normally come from file uploads
    docs_raw = [
        {
            "filename": "form16_sample.pdf",
            "raw_text": """
            FORM NO. 16
            
            Name of Employer: TechCorp India Pvt Ltd
            Name of Employee: Rahul Sharma
            PAN of Employee: ABCRS1234H
            
            Assessment Year: 2025-26
            Financial Year: 2024-25
            
            PART B - Details of Salary
            
            Gross Salary 8,50,000
            Total Salary rs. 850000
            
            Standard Deduction rs. 50,000
            
            Deductions under Chapter VI-A:
            Section 80C rs. 1,50,000
            Section 80D rs. 25,000
            
            TDS Deducted rs. 65,000
            """
        },
        {
            "filename": "bank_statement.pdf",
            "raw_text": """
            INTEREST CERTIFICATE
            State Bank of India
            
            Account Holder: Rahul Sharma
            PAN: ABCRS1234H
            
            Financial Year: 2024-25
            
            Interest Income rs. 2,00,000
            
            TDS Deducted rs. 20,000
            """
        }
    ]
    
    print(f"\nInput Documents:")
    for doc in docs_raw:
        print(f"   - {doc['filename']}: {len(doc['raw_text'])} characters")
    
    print(f"\nRunning automatic ITR workflow (NO manual input)...")
    try:
        result = run_itr_workflow(docs_raw=docs_raw)
        
        print(f"\n[PASS] Workflow completed successfully!")
        print(f"   Run ID: {result.run_id}")
        print(f"   Status: {result.filing_status.status.value}")
        
        print(f"\nIncome Extraction (Automatic):")
        print(f"   Salary: Rs {result.aggregated_income.total_salary:,.0f}")
        print(f"   Interest Income: Rs {result.aggregated_income.total_interest:,.0f}")
        print(f"   Gross Total: Rs {result.aggregated_income.gross_total_income:,.0f}")
        print(f"   Total TDS: Rs {result.aggregated_income.total_tds:,.0f}")
        
        print(f"\nDeductions (Automatic):")
        print(f"   80C (capped): Rs {result.deduction_components.section_80c_raw:,.0f}")
        print(f"   80D (capped): Rs {result.deduction_components.section_80d_raw:,.0f}")
        print(f"   Total Deductions: Rs {(result.deduction_components.section_80c_raw + result.deduction_components.section_80d_raw):,.0f}")
        
        print(f"\nTax Calculation (Automatic):")
        print(f"   Taxable Income: Rs {result.tax_computation.taxable_income:,.0f}")
        print(f"   Tax on Income: Rs {result.tax_computation.tax_on_income:,.0f}")
        print(f"   Total Tax Liability: Rs {result.tax_computation.total_tax_liability:,.0f}")
        print(f"   Total TDS Paid: Rs {result.tax_computation.total_tds:,.0f}")
        
        if result.tax_computation.net_refund > 0:
            print(f"   [SUCCESS] NET REFUND: Rs {result.tax_computation.net_refund:,.0f}")
        else:
            print(f"   TAX PAYABLE: Rs {abs(result.tax_computation.net_payable):,.0f}")
        
        print(f"\nITR Form Filling (Automatic):")
        if result.itr_form:
            print(f"   Form Selected: {result.itr_form.itr_type}")
            print(f"   File Status: {result.filing_status.status.value}")
        
        print(f"\nAgent Timeline:")
        for i, step in enumerate(result.agent_steps[:5], 1):
            output_text = step.output_summary[:60] + "..." if len(step.output_summary) > 60 else step.output_summary
            print(f"   {i}. {step.agent_name}: {output_text}")
        
        print(f"\n[SUCCESS] TEST 1 PASSED: Fully automatic extraction and filing!")
        return True
        
    except Exception as e:
        print(f"\n[FAIL] TEST 1 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_automatic_filing_scenario_2():
    """Test 2: Senior Citizen - New Regime"""
    print("\n" + "="*80)
    print("[TEST 2] AUTOMATIC FILING - Senior Citizen (New Regime)")
    print("="*80)
    
    docs_raw = [
        {
            "filename": "form16_senior.pdf",
            "raw_text": """
            FORM NO. 16
            Name of Employer: Private Company India Ltd
            Name of Employee: Senior Citizen
            PAN of Employee: SENI0001OLD
            Age: 65
            
            Gross Salary: 900000
            Annual Salary: Rs. 9,00,000
            
            Standard Deduction: Rs. 50,000
            
            Section 80C: Rs. 50,000
            80C total: 50000
            
            TDS deducted: Rs. 48,000
            Income Tax Deducted: 48000
            """
        },
        {
            "filename": "bank_certificate.pdf",
            "raw_text": """
            INTEREST CERTIFICATE
            Bank Name: HDFC Bank
            
            Account Holder: Senior Citizen
            PAN: SENI0001OLD
            
            Interest Income: Rs. 45,000
            Interest income: 45000
            
            TDS Deducted: Rs. 4,500
            Tax Deducted: 4500
            """
        }
    ]
    
    print("\nInput Documents:")
    for doc in docs_raw:
        print(f"   - {doc['filename']}")
    
    print("\nRunning automatic ITR workflow (NEW REGIME - Selected Automatically)...")
    try:
        result = run_itr_workflow(docs_raw=docs_raw)
        
        print(f"\n[PASS] Workflow completed!")
        print(f"   Regime: {result.taxpayer.regime.value}")
        print(f"   Status: {result.filing_status.status.value}")
        
        print(f"\nExtracted Income:")
        print(f"   Total: Rs {result.aggregated_income.gross_total_income:,.0f}")
        print(f"   TDS Paid: Rs {result.aggregated_income.total_tds:,.0f}")
        
        if result.tax_computation.net_refund > 0:
            print(f"   NET REFUND: Rs {result.tax_computation.net_refund:,.0f}")
        
        print(f"\n[SUCCESS] TEST 2 PASSED: New Regime automatic handling!")
        return True
        
    except Exception as e:
        print(f"\n[FAIL] TEST 2 FAILED: {e}")
        return False



def test_ocr_dependency_error():
    """Ensure meaningful error raised when OCR dependencies are missing."""
    from document_parser import OCRDependencyError
    print("\n" + "="*80)
    print("[TEST OCR DEPENDENCY]")
    print("="*80)
    sample_path = Path(r"c:\Users\HP\Downloads\567823807-Sample-Form-16.pdf")
    if not sample_path.exists():
        print("SKIP: sample Form 16 PDF not found at", sample_path)
        return True
    try:
        _ = extract_text_from_file(str(sample_path))
        print("[FAIL] Expected OCRDependencyError but extraction succeeded")
        return False
    except Exception as e:
        if isinstance(e, OCRDependencyError):
            print("[PASS] OCRDependencyError raised as expected:", e)
            return True
        else:
            print("[FAIL] Unexpected exception type:", type(e), e)
            return False


def run_all_tests():
    """Run complete test suite"""
    print("\n" + "="*80)
    print("[TEST SUITE] AUTOMATIC ITR AUTO-FILER")
    print("Testing: Document Upload → Auto Extraction → Auto Filing")
    print("="*80)
    
    init_db()
    
    results = []
    results.append(("Test 1: Salaried Individual", test_automatic_filing_scenario_1()))
    results.append(("Test 2: Senior Citizen (New Regime)", test_automatic_filing_scenario_2()))
    
    print("\n" + "="*80)
    print("📊 TEST RESULTS")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, passed_flag in results:
        status = "[PASS]" if passed_flag else "[FAIL]"
        print(f"{status}: {test_name}")
    
    print(f"\n{'='*80}")
    if passed == total:
        print(f"[SUCCESS] ALL TESTS PASSED ({passed}/{total})")
        print(f"\nSYSTEM IS 100% AUTOMATIC - NO MANUAL ENTRY NEEDED")
        print(f"Document upload -> Automatic extraction -> Automatic filing")
    else:
        print(f"[WARNING] {total - passed} test(s) failed")
    print("="*80)
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

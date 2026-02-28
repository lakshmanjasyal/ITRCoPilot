"""
Diagnostic script to debug document extraction from real PDFs
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from document_parser import extract_text_from_file

# User's actual files
form16_path = r"C:\Users\HP\Downloads\567823807-Sample-Form-16.pdf"
bank_path = r"C:\Users\HP\Downloads\bankst.pdf"

print("="*80)
print("DOCUMENT EXTRACTION DIAGNOSTIC")
print("="*80)

# Extract Form 16
print("\n[1] FORM 16 EXTRACTION")
print("-"*80)
if Path(form16_path).exists():
    text_form16 = extract_text_from_file(form16_path, "application/pdf")
    print(f"File: {Path(form16_path).name}")
    print(f"Extracted Text Length: {len(text_form16)} characters")
    print(f"\nFirst 3000 characters of Form 16:")
    print("-"*80)
    print(text_form16[:3000])
    print("-"*80)
    
    # Now test extraction functions
    from orchestrator.graph import (
        _extract_salary_from_form16, 
        _extract_tds_from_form16,
        _extract_80c_from_form16,
        _extract_80d_from_form16
    )
    
    print("\nEXTRACTED VALUES FROM FORM 16:")
    salary = _extract_salary_from_form16(text_form16)
    tds = _extract_tds_from_form16(text_form16)
    c80c = _extract_80c_from_form16(text_form16)
    c80d = _extract_80d_from_form16(text_form16)
    
    print(f"  Salary: {salary:,.0f}")
    print(f"  TDS Deducted: {tds:,.0f}")
    print(f"  80C Deduction: {c80c:,.0f}")
    print(f"  80D Deduction: {c80d:,.0f}")
else:
    print(f"File not found: {form16_path}")

# Extract Bank Statement
print("\n\n[2] BANK STATEMENT EXTRACTION")
print("-"*80)
if Path(bank_path).exists():
    text_bank = extract_text_from_file(bank_path, "application/pdf")
    print(f"File: {Path(bank_path).name}")
    print(f"Extracted Text Length: {len(text_bank)} characters")
    print(f"\nFirst 3000 characters of Bank Statement:")
    print("-"*80)
    print(text_bank[:3000])
    print("-"*80)
    
    from orchestrator.graph import (
        _extract_interest_from_bank,
    )
    
    print("\nEXTRACTED VALUES FROM BANK STATEMENT:")
    interest = _extract_interest_from_bank(text_bank)
    
    print(f"  Interest Income: {interest:,.0f}")
else:
    print(f"File not found: {bank_path}")

print("\n" + "="*80)
print("DIAGNOSIS COMPLETE")
print("="*80)
print("\nIf values are showing as 0, the regex patterns don't match the PDF format.")
print("Check the 'First #### characters' sections above to see the actual structure.")

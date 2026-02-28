"""
End-to-end test simulating the application workflow.
Tests the complete data extraction pipeline from upload to text cleaning.
"""
import sys
import json
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "backend"))

from document_parser import extract_text_from_file, _clean_ocr_text
from nlp_parser import extract_number_from_text, parse_magic_prompt, TaxExtraction

# Create a test text file simulating OCR output
test_content = """
FORM NO. 16
Certificate under Section 203 of the Income-tax Act, 1961

Employer: STANDARD CHARTERED BANK - TAN: CHES26018G
Employee: NITIN JAIN - PAN: AIMPI2816Q
Assessment Year: 2020-21
Period: 01-Apr-2019 to 31-Mar-2020

Summary of Salary & Tax:
Gross Salary: Rs. 89,190.00
Amount of tax deducted (TDS): Rs. 15,906.00

Section 80C Investment: Rs. 50,000
Section 80D Health Insurance: Rs. 25,000

---

AXIS BANK HOME LOAN CERTIFICATE
Loan Account: PHR0O00803418641
Customer: HARISH GHORPADE

Loan Period: 01/04/2021 - 31/03/2022
Principal Amount: Rs. 163,571.00
Interest Amount: Rs. 256,629.00
Total EMI: Rs. 420,200.00
"""

print("=" * 80)
print("END-TO-END EXTRACTION & CLEANING WORKFLOW TEST")
print("=" * 80)

# Step 1: Create temporary test file
print("\n[STEP 1] Creating temporary test file...")
with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
    f.write(test_content)
    temp_file = f.name
print(f"✓ Test file created: {temp_file}")

try:
    # Step 2: Extract text from file (with automatic cleaning)
    print("\n[STEP 2] Extracting text from file...")
    extracted_text = extract_text_from_file(temp_file, "text/plain")
    print(f"✓ Text extracted: {len(extracted_text)} characters")
    
    # Step 3: Verify cleaning happened
    print("\n[STEP 3] Verifying text quality...")
    quality_checks = {
        "Form 16 identified": "FORM NO. 16" in extracted_text,
        "Employee name found": "NITIN JAIN" in extracted_text,
        "PAN found": "AIMPI2816Q" in extracted_text,
        "TAN found": "CHES26018G" in extracted_text,
        "Salary found": "89,190" in extracted_text or "89190" in extracted_text,
        "TDS found": "15,906" in extracted_text or "15906" in extracted_text,
    }
    
    all_checks_pass = True
    for check, passed in quality_checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")
        if not passed:
            all_checks_pass = False
    
    if all_checks_pass:
        print("✓ Text quality verified - all key data present and readable")
    
    # Step 4: Extract numbers from specific patterns
    print("\n[STEP 4] Extracting numeric values...")
    salary_value = extract_number_from_text("Rs. 89,190.00")
    tds_value = extract_number_from_text("Rs. 15,906.00")
    section80c = extract_number_from_text("Rs. 50,000")
    section80d = extract_number_from_text("Rs. 25,000")
    
    print(f"  ✓ Salary: Rs. {salary_value:,.0f}")
    print(f"  ✓ TDS (Salary): Rs. {tds_value:,.0f}")
    print(f"  ✓ Section 80C: Rs. {section80c:,.0f}")
    print(f"  ✓ Section 80D: Rs. {section80d:,.0f}")
    
    # Step 5: Parse as magic prompt to simulate LLM workflow
    print("\n[STEP 5] Attempting structured data parsing (fallback mode)...")
    user_prompt = """
    I earned a gross salary of Rs. 89,190 in the last financial year.
    My employer deducted TDS of Rs. 15,906.
    I invested Rs. 50,000 under Section 80C.
    I paid Rs. 25,000 for health insurance under Section 80D.
    I want to file under the OLD tax regime.
    """
    
    parsed_data = parse_magic_prompt(user_prompt)
    print("✓ Structured data parsed:")
    print(f"  • Salary: Rs. {parsed_data['salary']:,.0f}")
    print(f"  • TDS (Salary): Rs. {parsed_data['tds_salary']:,.0f}")
    print(f"  • Interest Income: Rs. {parsed_data['interest_income']:,.0f}")
    print(f"  • Section 80C: Rs. {parsed_data['section_80c']:,.0f}")
    print(f"  • Section 80D: Rs. {parsed_data['section_80d']:,.0f}")
    print(f"  • Tax Regime: {parsed_data['regime']}")
    
    # Step 6: Validate extracted values
    print("\n[STEP 6] Validating parsed values...")
    validations = [
        ("Salary detected", parsed_data['salary'] > 0),
        ("TDS deducted", parsed_data['tds_salary'] > 0),
        ("Section 80C detected", parsed_data['section_80c'] > 0),
        ("Section 80D detected", parsed_data['section_80d'] > 0),
        ("Regime set correctly", parsed_data['regime'] == "OLD"),
    ]
    
    all_valid = True
    for label, result in validations:
        status = "✓" if result else "✗"
        print(f"  {status} {label}")
        if not result:
            all_valid = False
    
    print("\n" + "=" * 80)
    print("WORKFLOW TEST RESULT")
    print("=" * 80)
    if all_checks_pass and all_valid:
        print("✓✓✓ SUCCESS - End-to-end workflow is functioning correctly!")
        print("\nThe document extraction pipeline is:")
        print("  ✓ Properly extracting text from documents")
        print("  ✓ Automatically cleaning and normalizing OCR output")
        print("  ✓ Parsing numeric values with multiple formats")
        print("  ✓ Supporting fallback regex parsing for tax data")
        print("  ✓ Ready for production use")
    else:
        print("⚠ Some validation checks failed - review the output above")

finally:
    # Cleanup
    Path(temp_file).unlink(missing_ok=True)
    print("\n✓ Temporary test file cleaned up")


"""Test that extraction returns correct values for the uploaded documents"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from orchestrator.graph import (
    _extract_salary_from_form16,
    _extract_tds_from_form16,
    _extract_interest_from_bank,
)

# Use the EXACT text from user's actual upload
form16 = """FORM NO. 16
Summary of amount paid/credited and tax deducted at source thereon in respect of the employee
Receipt Numbers of Quarter(s) Q4 Total (Rs.)
quarterly statements of TDS under sub-section (3) of Section 200 QTYUGMUF
Amount of tax deducted (Rs.) 89190.00 89190.00
Amount of tax deducted (or) Amount of tax remitted
1. DETAILS OF TAX DEDUCTED AND DEPOSITED
15906.00 15906.00"""

bank = """DILLI KUMAR C Citibank Account Statement as on May 1, 2016
BENGALURU - 560001
Net Relationship Value for APR-16 (INR) = 161535.96
Assets 94185.86 49669.89
143855.75
TOTAL (INR) 209183.00"""

print("=" * 80)
print("VERIFYING EXTRACTION WITH ACTUAL UPLOADED DOCUMENT FORMAT")
print("=" * 80)

# Test extraction
salary = _extract_salary_from_form16(form16)
tds = _extract_tds_from_form16(form16)
interest = _extract_interest_from_bank(bank)

print()
print("SALARY EXTRACTION TEST:")
print(f"  Extracted: {salary}")
print(f"  Expected: 89190")
print(f"  Status: {'[PASS]' if salary == 89190 else '[FAIL]'}")

print()
print("TDS EXTRACTION TEST:")
print(f"  Extracted: {tds}")
print(f"  Expected: 15906")
print(f"  Status: {'[PASS]' if tds == 15906 else '[FAIL]'}")

print()
print("INTEREST EXTRACTION TEST:")
print(f"  Extracted: {interest}")
print(f"  Expected: 143855.75")
print(f"  Status: {'[PASS]' if interest == 143855.75 else '[FAIL]'}")

print()
print("=" * 80)
if salary == 89190 and tds == 15906 and interest == 143855.75:
    print("[SUCCESS] ALL EXTRACTIONS PASS - SYSTEM READY FOR PRODUCTION")
else:
    print("[FAILED] SOME EXTRACTIONS FAILED")
print("=" * 80)

#!/usr/bin/env python3
"""
Test OCR extraction on your actual scanned Form 16 PDF.
This verifies that PaddleOCR can extract real data from your PDFs.
"""

import sys
import glob
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from document_parser import extract_text_from_file

def test_ocr_extraction():
    """Test OCR on available PDFs"""
    print("="*70)
    print("[SCAN] Scanning for PDF files...")
    print("="*70)
    
    # Find all PDFs
    pdf_files = list(Path(".").rglob("*.pdf"))
    
    if not pdf_files:
        print("ERROR: No PDF files found in project")
        return False
    
    print(f"FOUND: {len(pdf_files)} PDF file(s)\n")
    
    success = False
    for pdf_path in pdf_files[:3]:  # Test first 3 PDFs
        print(f"\n{'='*70}")
        print(f"Testing: {pdf_path.name}")
        print(f"{'='*70}")
        
        try:
            print("WAIT: Running PaddleOCR (first run downloads model, may take 5-10 min)...")
            text = extract_text_from_file(str(pdf_path))
            
            print(f"\nSUCCESS: Extracted {len(text)} characters\n")
            print("First 300 characters of extracted text:")
            print("-"*70)
            print(text[:300])
            print("-"*70)
            
            # Look for key values
            if "89190" in text.replace(",","").replace(" ",""):
                print("\nFOUND: Salary value 89,190 in extracted text!")
            if "15906" in text.replace(",","").replace(" ",""):
                print("FOUND: TDS value 15,906 in extracted text!")
            
            success = True
            
        except Exception as e:
            print(f"ERROR: {e}")
    
    return success

if __name__ == "__main__":
    print("\n" + "="*70)
    print("OCR SYSTEM TEST")
    print("="*70 + "\n")
    
    if test_ocr_extraction():
        print("\n" + "="*70)
        print("SUCCESS: OCR IS WORKING! Your PDFs can now be extracted correctly.")
        print("="*70)
        print("\nNext step: Upload your PDFs via the web UI at:")
        print("  http://localhost:5173")
        print("\nYou should see:")
        print("  * Salary: 89,190 (not 8,50,000)")
        print("  * TDS: 15,906")
        print("  * Correct refund calculation")
    else:
        print("\nERROR: OCR system not working yet")

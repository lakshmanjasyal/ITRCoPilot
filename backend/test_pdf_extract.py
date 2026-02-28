import PyPDF2

pdf_path = r"c:\Users\HP\Downloads\567823807-Sample-Form-16.pdf"
try:
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        print(f"Total pages: {len(reader.pages)}")
        print("\n=== First page text (first 2000 chars) ===")
        text = reader.pages[0].extract_text()
        if text:
            print(text[:2000])
            print("\n=== Looking for salary/TDS keywords ===")
            text_lower = text.lower()
            if "salary" in text_lower:
                print("✓ Found 'salary'")
            if "tds" in text_lower:
                print("✓ Found 'tds'")
            if "80c" in text_lower or "80-c" in text_lower:
                print("✓ Found '80c'")
            print(f"\nTotal characters extracted: {len(text)}")
        else:
            print("No text extracted")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

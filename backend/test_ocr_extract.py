from document_parser import extract_text_from_file

pdf_path = r"c:\Users\HP\Downloads\567823807-Sample-Form-16.pdf"
try:
    text = extract_text_from_file(pdf_path)
except Exception as e:
    print(f"Error during extraction: {e}")
    raise

print(f"Extracted text length: {len(text)} characters")
print("\n=== First 3000 characters ===")
print(text[:3000])

# Check for key fields
text_lower = text.lower()
print("\n=== Key fields found ===")
print(f"'salary' found: {'salary' in text_lower}")
print(f"'tds' found: {'tds' in text_lower}")
print(f"'80c' found: {'80c' in text_lower or '80-c' in text_lower}")
print(f"'80d' found: {'80d' in text_lower or '80-d' in text_lower}")

# Extract some sample lines with numbers
import re
numbers = re.findall(r'\d[\d,]*(?:\.\d+)?', text)
print(f"\n=== Sample numbers extracted ===")
for i, num in enumerate(numbers[:20]):
    print(f"{i+1}. {num}")

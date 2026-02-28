import sys
sys.path.insert(0, r'c:\Users\HP\Desktop\ksum\backend')
from document_parser import extract_text_from_file
import glob

pdfs = glob.glob(r'c:\Users\HP\Desktop\ksum\**\*.pdf', recursive=True)
if pdfs:
    pdf = pdfs[0]
    print(f'Testing PDF: {pdf.split(chr(92))[-1]}')
    try:
        text = extract_text_from_file(pdf)
        print(f'\nSUCCESS: Extracted {len(text)} characters')
        print('\nFirst 400 characters:')
        print(text[:400])
        
        # Check for salary values
        if '89190' in text.replace(',','').replace(' ',''):
            print('\nFOUND: Your salary 89,190!')
        if '15906' in text.replace(',','').replace(' ',''):
            print('FOUND: Your TDS 15,906!')
    except Exception as e:
        print(f'ERROR: {str(e)[:300]}')

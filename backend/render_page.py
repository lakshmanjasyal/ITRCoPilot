import fitz

pdf_path = r"c:\Users\HP\Downloads\567823807-Sample-Form-16.pdf"

try:
    doc = fitz.open(pdf_path)
    print("pages", len(doc))
    page = doc[0]
    pix = page.get_pixmap(dpi=300)
    out = r"c:\Users\HP\Desktop\ksum\backend\page0.png"
    pix.save(out)
    print("saved page image to", out)
except Exception as e:
    print("error", e)
    import traceback; traceback.print_exc()

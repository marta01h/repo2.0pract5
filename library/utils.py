import fitz  # PyMuPDF

def convert_pdf_to_markdown(pdf_path):
    doc = fitz.open(pdf_path)
    text = "\n\n".join([page.get_text("text") for page in doc])
    return text if text.strip() else "Нет текста в PDF"

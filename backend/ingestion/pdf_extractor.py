import PyPDF2

def extract_pdf(path: str) -> str:
    """Extract text from a PDF file."""
    text = ""
    with open(path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            try:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            except:
                continue
    return text

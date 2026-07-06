import os
from pypdf import PdfReader
from docx import Document
from PIL import Image
import pytesseract

# Tell pytesseract exactly where Tesseract is installed on Windows
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# --- PDF Loader ---

def load_pdf(file_path):
    reader = PdfReader(file_path)
    full_text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            full_text += page_text + "\n"
    return full_text

# --- TXT Loader ---

def load_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# --- DOCX Loader ---

def load_docx(file_path):
    doc = Document(file_path)
    full_text = ""
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            full_text += paragraph.text + "\n"
    return full_text

# --- Image Loader (OCR) ---

def load_image(file_path):
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    return text

# --- Master Loader ---
# Detects file type automatically and calls the right loader

def load_document(file_path):

    # Get the file extension in lowercase
    extension = os.path.splitext(file_path)[1].lower()

    print(f"Loading {extension} file: {os.path.basename(file_path)}")

    if extension == ".pdf":
        text = load_pdf(file_path)

    elif extension == ".txt":
        text = load_txt(file_path)

    elif extension == ".docx":
        text = load_docx(file_path)

    elif extension in [".png", ".jpg", ".jpeg"]:
        text = load_image(file_path)

    else:
        raise ValueError(f"Unsupported file type: {extension}")

    # Clean up excessive whitespace
    text = " ".join(text.split())

    if not text.strip():
        raise ValueError(f"No text could be extracted from {os.path.basename(file_path)}")

    print(f"Successfully extracted {len(text)} characters")
    return text


# --- Quick Test ---

if __name__ == "__main__":

    import sys

    if len(sys.argv) < 2:
        print("Usage: python loader.py <path_to_file>")
        print("Example: python loader.py mydocument.pdf")
    else:
        file_path = sys.argv[1]
        text = load_document(file_path)
        print(f"\nFirst 300 characters:\n{text[:300]}")
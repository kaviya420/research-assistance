import fitz  # PyMuPDF
import pdfplumber
import io
from langchain_text_splitters import RecursiveCharacterTextSplitter

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extracts text from a PDF given as bytes."""
    print(f"INFO: Attempting to extract text from file of size {len(file_bytes)} bytes.")
    
    if len(file_bytes) < 100:
        print("ERROR: File is too small to be a valid PDF.")
        return ""
        
    # Check if it's actually an HTML file disguised as PDF (common with direct downloads)
    if b"<html" in file_bytes[:500].lower() or b"<!doctype html>" in file_bytes[:500].lower():
        print("ERROR: This file appears to be an HTML webpage, not a valid PDF. The download probably failed.")
        raise ValueError("The uploaded file is an HTML page (likely an error page), not a valid PDF document. Please download the PDF directly using the download button on the arXiv page.")

    text = ""
    # Try using PyMuPDF first for speed
    try:
        pdf = fitz.open(stream=file_bytes, filetype="pdf")
        for page_num in range(len(pdf)):
            page = pdf.load_page(page_num)
            page_text = page.get_text("text")
            if page_text:
                text += page_text + "\n"
        print(f"INFO: fitz (PyMuPDF) successfully extracted {len(text)} characters.")
    except Exception as e:
        print(f"PyMuPDF failed: {e}")
        try:
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
                print(f"INFO: pdfplumber successfully extracted {len(text)} characters.")
        except Exception as e2:
            print(f"pdfplumber also failed: {e2}")
    
    return text

def chunk_text(text: str, chunk_size=1000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    return splitter.split_text(text)

# app/loader.py

import os

import pytesseract
from pdf2image import convert_from_path

# Set correct path to Tesseract binary
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Set path to 'tessdata' folder (⚠️ very important!)
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"


def extract_text_from_pdf_ocr(pdf_path: str, lang="ben") -> str:
    """
    Extract text from a scanned PDF using OCR (Tesseract).
    :param pdf_path: Path to PDF file
    :param lang: Language code for OCR ('ben' for Bangla)
    :return: Extracted text as string
    """
    images = convert_from_path(pdf_path, dpi=300)  # Convert PDF to images
    all_text = []

    for i, img in enumerate(images):
        print(f"🔍 OCR processing page {i+1} of {len(images)}")
        text = pytesseract.image_to_string(img, lang=lang)
        all_text.append(text.strip())

    return "\n\n".join(all_text)

import re


def clean_ocr_text(raw_text: str) -> str:
    """
    Cleans raw OCR text by removing unnecessary whitespace, fixing common OCR errors,
    and standardizing formatting for better chunking.
    """
    # Remove extra newlines and normalize spaces
    # Collapse multiple newlines
    text = re.sub(r"\n+", "\n", raw_text)
    # Collapse multiple spaces/tabs
    text = re.sub(r"[ \t]+", " ", text)
    # Remove trailing spaces before newline
    text = re.sub(r" +\n", "\n", text)
    # Remove leading spaces after newline
    text = re.sub(r"\n +", "\n", text)

    # Optional: fix some common OCR errors (customizable)
    # Fix misplaced Bangla vowel signs
    text = text.replace("ি ", "ি")
    # Remove space after Bangla "hasanta"
    text = text.replace("্ ", "্")
    # Remove non-breaking or weird spaces
    text = re.sub(r"[^\S\r\n]+", " ", text)

    # Remove page numbers or broken headers (optional, depends on your PDF layout)
    text = re.sub(r"\s*Page\s+\d+\s*", "", text, flags=re.IGNORECASE)

    # Strip outer whitespace
    return text.strip()

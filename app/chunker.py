from typing import List


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split text into overlapping chunks of a fixed size.

    Args:
        text (str): The input cleaned text.
        chunk_size (int): Number of characters per chunk.
        overlap (int): Number of overlapping characters between chunks.

    Returns:
        List[str]: List of text chunks.
    """
    chunks = []
    start = 0
    length = len(text)

    while start < length:
        end = min(start + chunk_size, length)
        chunk = text[start:end].strip()
        chunks.append(chunk)
        start += chunk_size - overlap  # move forward with overlap

    return chunks

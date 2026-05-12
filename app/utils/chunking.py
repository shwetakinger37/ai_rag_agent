from typing import List


def split_text(text: str, chunk_size: int = 1000, overlap: int = 150) -> List[str]:
    """Simple character-based chunking with overlap."""
    clean_text = " ".join(text.split())
    if not clean_text:
        return []

    chunks = []
    start = 0
    while start < len(clean_text):
        end = start + chunk_size
        chunk = clean_text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap
        if start < 0:
            start = 0
        if start >= len(clean_text):
            break
    return chunks

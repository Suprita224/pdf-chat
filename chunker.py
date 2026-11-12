import os
import sys

from pypdf import PdfReader


def load_pdf(path):
    """Return a list of (page_number, text) for every page of the PDF."""
    reader = PdfReader(path)
    pages = []
    for number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = text.replace("\ufffd", "-")  # unreadable bullet symbols
        pages.append((number, text))
    return pages


def chunk_text(text, size=800, overlap=150):
    """Split text into overlapping chunks, cutting at sentence or word boundaries."""
    text = " ".join(text.split())  # collapse newlines and repeated spaces
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text):
            cut = text.rfind(". ", start, end)
            if cut == -1 or cut < start + size // 2:
                cut = text.rfind(" ", start, end)
            if cut > start:
                end = cut + 1
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
    return chunks


def build_chunks(path):
    """Return a list of dicts: id, text, source file name, page number."""
    source = os.path.basename(path)
    result = []
    for page_number, text in load_pdf(path):
        for i, chunk in enumerate(chunk_text(text)):
            result.append(
                {
                    "id": f"{source}-p{page_number}-c{i}",
                    "text": chunk,
                    "source": source,
                    "page": page_number,
                }
            )
    return result


if __name__ == "__main__":
    chunks = build_chunks(sys.argv[1])
    lengths = [len(c["text"]) for c in chunks]
    print("Chunks:", len(chunks))
    print("Average length:", sum(lengths) // len(lengths), "characters")
    print("Shortest:", min(lengths), "Longest:", max(lengths))
    sample = chunks[len(chunks) // 2]
    print("\nSample chunk from page", sample["page"], ":")
    print(sample["text"])

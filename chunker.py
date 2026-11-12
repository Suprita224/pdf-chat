import os
import re
import sys
from collections import Counter

from pypdf import PdfReader


def normalize_line(line):
    # "Page 15 of 31" and "Page 16 of 31" become the same line, so repeats are detected
    return re.sub(r"\d+", "#", line.strip())


def load_pdf(path):
    """Return a list of (page_number, text) with repeated headers and footers removed."""
    reader = PdfReader(path)
    raw = []
    for number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = text.replace("\ufffd", "-")  # unreadable bullet symbols
        raw.append((number, text))

    # a line that appears on at least half of the pages is a header or footer
    counts = Counter()
    for _, text in raw:
        for line in {normalize_line(l) for l in text.splitlines() if l.strip()}:
            counts[line] += 1
    limit = max(3, len(raw) // 2)
    repeated = {line for line, n in counts.items() if n >= limit}

    pages = []
    for number, text in raw:
        kept = [l for l in text.splitlines() if normalize_line(l) not in repeated]
        pages.append((number, "\n".join(kept)))
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
        nxt = text.find(" ", start, end)  # begin the next chunk at a word boundary
        if nxt != -1:
            start = nxt + 1
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

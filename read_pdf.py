import sys

from pypdf import PdfReader

reader = PdfReader(sys.argv[1])
print("Pages:", len(reader.pages))

for number, page in enumerate(reader.pages, start=1):
    text = page.extract_text() or ""
    print(f"--- page {number}: {len(text)} characters ---")
    print(text[:200])
    if number == 3:  # only show the first 3 pages for now
        break

import sys

import chromadb

from chunker import build_chunks

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="documents")


def index_pdf(path):
    chunks = build_chunks(path)
    source = chunks[0]["source"]
    # remove old entries for this file so re-indexing never creates duplicates
    collection.delete(where={"source": source})
    batch = 100
    for i in range(0, len(chunks), batch):
        part = chunks[i : i + batch]
        collection.add(
            ids=[c["id"] for c in part],
            documents=[c["text"] for c in part],
            metadatas=[{"source": c["source"], "page": c["page"]} for c in part],
        )
    return len(chunks)


if __name__ == "__main__":
    n = index_pdf(sys.argv[1])
    print(f"Indexed {n} chunks. Total in database: {collection.count()}")

import sys

import chromadb

client = chromadb.PersistentClient(path="chroma_db")


def search(question, k=4):
    """Return the k chunks closest in meaning to the question."""
    collection = client.get_or_create_collection(name="documents")
    result = collection.query(query_texts=[question], n_results=k)
    hits = []
    for i in range(len(result["ids"][0])):
        hits.append(
            {
                "text": result["documents"][0][i],
                "source": result["metadatas"][0][i]["source"],
                "page": result["metadatas"][0][i]["page"],
                "distance": result["distances"][0][i],
            }
        )
    return hits


if __name__ == "__main__":
    question = " ".join(sys.argv[1:])
    for rank, hit in enumerate(search(question), start=1):
        print(f"\n#{rank}  {hit['source']}  page {hit['page']}  (distance {hit['distance']:.2f})")
        print(hit["text"][:300] + "...")

import sys

import requests

from search import search

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:1b"  # change this one line to try a different model

SYSTEM = (
    "You answer questions using ONLY the context excerpts provided. "
    "Each excerpt starts with a label like [notes.pdf, page 4]. "
    "Cite the pages you used in your answer, like (page 4). "
    "If the context does not contain the answer, reply exactly: "
    "I could not find that in the document."
)


def build_prompt(question, hits):
    parts = []
    for h in hits:
        parts.append(f"[{h['source']}, page {h['page']}]\n{h['text']}")
    context = "\n\n".join(parts)
    return f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"


def ask_llm(question, hits):
    payload = {
        "model": MODEL,
        "stream": False,
        "options": {"temperature": 0},  # 0 = the most predictable answers
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": build_prompt(question, hits)},
        ],
    }
    response = requests.post(OLLAMA_URL, json=payload, timeout=300)
    response.raise_for_status()
    return response.json()["message"]["content"].strip()


def answer(question, k=4):
    hits = search(question, k=k)
    text = ask_llm(question, hits)
    pages = sorted({h["page"] for h in hits})
    return {"answer": text, "pages": pages, "hits": hits}


if __name__ == "__main__":
    question = " ".join(sys.argv[1:])
    result = answer(question)
    print("\nAnswer:", result["answer"])
    print("Pages searched:", result["pages"])

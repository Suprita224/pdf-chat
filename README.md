# Chat with Your PDFs

A local retrieval-augmented generation (RAG) app. Upload PDFs, ask questions in a chat box, and get an answer plus the exact passages and page numbers the search found. Everything runs on your own machine: no API key and no data sent to a third party.

## Features

- Upload and index multiple PDFs from a Streamlit web page
- Semantic search over page-aware text chunks (ChromaDB with a local embedding model)
- Answers written by a local LLM (Ollama, `llama3.2:1b`) from the retrieved passages only
- A Sources panel under every answer, with the file name, page number, and original text
- Refuses off-topic questions using a similarity cutoff, before the model is called
- Measured retrieval quality with a labelled test set (see Evaluation)

## How it works

1. `chunker.py` reads each PDF page with pypdf, removes headers and footers that repeat on many pages, and splits the text into overlapping chunks of about 800 characters. Chunks never cross a page, so each one keeps a correct page number.
2. `index.py` stores the chunks in ChromaDB, which turns each chunk into an embedding (all-MiniLM-L6-v2, running locally).
3. `search.py` embeds the question and returns the 4 closest chunks.
4. `answer.py` refuses if even the closest chunk is farther than a distance cutoff. Otherwise it sends the chunks to the local model with instructions to answer only from them.
5. `app.py` is the Streamlit interface.

## Run it

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

    curl -fsSL https://ollama.com/install.sh | sh
    ollama pull llama3.2:1b

    streamlit run app.py

Upload a PDF in the sidebar and click "Index uploaded files". To index from the command line instead: `python3 index.py docs/yourfile.pdf`.

## Evaluation

I wrote 21 questions about a 31-page project report: 17 whose answers appear on known pages (the labels were drafted with AI assistance and spot-checked by me against the PDF) and 4 off-topic questions. A hit means a chunk from a correct page was among the top 4 results.

| Metric | Result |
|---|---|
| Hit@4 | 15/17 (88%) |
| Hit@1 | 10/17 (59%) |
| MRR | 0.72 |
| Best distance, answerable questions | 0.70 to 1.55 |
| Best distance, off-topic questions | 1.59 to 1.85 |

The distance ranges do not overlap, so a cutoff of 1.57 refused all 4 off-topic questions and none of the 17 answerable ones. Caveats: the cutoff was tuned on the same small set it was measured on, and it depends on the document and the embedding model, so it is a single constant (`MAX_DISTANCE` in `answer.py`) that should be re-tuned for a new corpus. `eval_set.py` is written for a private report that is not included in this repository; replace its questions and page numbers with ones for your own PDF, then run `python3 eval.py`.

**The two misses** were generically worded questions ("what is the main question the project is trying to answer", "what must the records show before expanding"). Other chunks about questions and records ranked above the right ones: the small embedding model matches meaning, not exact phrases.

## Findings and limitations

- A 1B-parameter local model sometimes mixes facts from different chunks and cites wrong page numbers in its own text. That is why the Sources panel is built from the search results, not from the model's output.
- The model can contradict itself on terms that appear only in a title.
- Scanned PDFs without a text layer are not supported (no OCR).
- Answer latency is roughly 10 to 60 seconds on a CPU-only laptop.

## Design decisions

- **Page-aware chunks with overlap:** keeps citations correct and avoids losing a sentence at a chunk boundary.
- **Header and footer removal:** lines repeated on at least half of the pages are dropped, because repeated text made unrelated chunks look similar.
- **Retrieval evaluated separately from generation:** if search returns the wrong page, the answer will be wrong, so retrieval is measured on its own.
- **Refusal before generation:** a distance cutoff stops the model from inventing answers to questions the document cannot answer.
- **Local by default:** the model name is one constant, so a hosted model can be swapped in.

## Future work

- Hybrid search (keyword plus embeddings) and a reranker to fix generic-question misses
- A larger evaluation set, with a separate set for tuning the cutoff
- Larger or hosted model for better answers
- OCR for scanned documents

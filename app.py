import os

import streamlit as st

from answer import answer
from index import collection, index_pdf

st.set_page_config(page_title="Chat with your PDFs")
st.title("Chat with your PDFs")

os.makedirs("docs", exist_ok=True)

with st.sidebar:
    st.header("Documents")
    uploaded = st.file_uploader(
        "Upload PDF files", type="pdf", accept_multiple_files=True
    )
    if uploaded and st.button("Index uploaded files"):
        for file in uploaded:
            path = os.path.join("docs", file.name)
            with open(path, "wb") as f:
                f.write(file.getbuffer())
            with st.spinner(f"Indexing {file.name}..."):
                count = index_pdf(path)
            st.success(f"{file.name}: {count} chunks")

    stored = collection.get(include=["metadatas"])
    names = sorted({m["source"] for m in stored["metadatas"]})
    st.write(f"Indexed documents ({len(names)}):")
    for name in names:
        st.write("- " + name)

if "history" not in st.session_state:
    st.session_state.history = []

for item in st.session_state.history:
    with st.chat_message("user"):
        st.write(item["question"])
    with st.chat_message("assistant"):
        st.write(item["answer"])
        with st.expander("Sources (found by the search, not written by the model)"):
            for hit in item["hits"]:
                st.markdown(
                    f"**{hit['source']}, page {hit['page']}** "
                    f"(distance {hit['distance']:.2f})"
                )
                st.write(hit["text"])

question = st.chat_input("Ask a question about your documents")
if question:
    if not names:
        st.warning("Upload and index a PDF first.")
    else:
        with st.spinner("Thinking..."):
            result = answer(question)
        st.session_state.history.append(
            {
                "question": question,
                "answer": result["answer"],
                "hits": result["hits"],
            }
        )
        st.rerun()


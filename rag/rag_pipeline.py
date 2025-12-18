import os
import numpy as np
import faiss
import tempfile
import textwrap
import streamlit as st
from pypdf import PdfReader
from transformers import AutoTokenizer, AutoModel, pipeline
import torch

def load_uploaded_files(uploaded_files):
    """
    Reads text from uploaded PDF and TXT files (Streamlit uploads).
    """
    all_text = ""

    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[1].lower()

        if file_ext == ".pdf":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(file.read())
                reader = PdfReader(tmp.name)
                for page in reader.pages:
                    if page.extract_text():
                        all_text += page.extract_text() + "\n"

        elif file_ext == ".txt":
            all_text += file.read().decode("utf-8", errors="ignore") + "\n"

        else:
            raise ValueError("Only PDF and TXT files are supported")

    return all_text


def chunk_text(text, chunk_size=450, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks

model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)


def get_embedding(text):
    tokens = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True
    )

    with torch.no_grad():
        outputs = model(**tokens)

    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()


def create_vector_store(chunks):
    print("⚙️ Creating embeddings...")
    embeddings = [get_embedding(chunk) for chunk in chunks]

    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    print(f"✅ Added {len(chunks)} chunks to FAISS index")
    return index


def retrieve_and_answer(query, index, chunks, qa_pipe, top_k=3):
    query_embedding = get_embedding(query).reshape(1, -1)
    _, indices = index.search(query_embedding, top_k)

    retrieved_chunks = [chunks[i] for i in indices[0]]
    context = "\n".join(retrieved_chunks)

    prompt = f"""
Answer ONLY from the context below.
If the answer is not present, say "Not found in document".

Context:
{context}

Question:
{query}
"""

    result = qa_pipe(prompt, max_new_tokens=200)
    return result[0]["generated_text"]

def initialize_pipeline(uploaded_files):
    print("📂 Reading uploaded documents...")
    document_text = load_uploaded_files(uploaded_files)

    print("✂️ Chunking text...")
    chunks = chunk_text(document_text)

    index = create_vector_store(chunks)
    qa_pipe = pipeline("text2text-generation", model="google/flan-t5-small")

    print("🤖 RAG pipeline ready!")
    return index, chunks, qa_pipe

uploaded_files = st.file_uploader(
    "Upload PDF or TXT files",
    type=["pdf", "txt"],
    accept_multiple_files=True
)

if uploaded_files:
    index, chunks, qa_pipe = initialize_pipeline(uploaded_files)

    question = st.text_input("Ask a question")
    if st.button("Get Answer"):
        answer = retrieve_and_answer(
            question, index, chunks, qa_pipe
        )
        st.write(answer)

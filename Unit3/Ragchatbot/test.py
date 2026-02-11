import streamlit as st

st.title("PDF Test")

uploaded = st.file_uploader("Upload PDF", type="pdf")

if uploaded:
    from langchain_community.document_loaders import PyPDFLoader
    import os, tempfile

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded.read())
        path = tmp.name

    loader = PyPDFLoader(path)
    docs = loader.load()

    st.success(f"Loaded {len(docs)} pages")

# PDF-Based RAG Chatbot with Memory (Groq / Cohere / HuggingFace)

This project demonstrates a **Retrieval Augmented Generation (RAG)**
chatbot that answers questions from uploaded PDF documents using
**open-source and non-OpenAI providers**. It is intended for **learning
and training purposes**.

------------------------------------------------------------------------

## Features

-   Upload PDF files via Streamlit UI
-   Chunking and embedding of PDF text
-   Vector storage using FAISS
-   Conversational memory
-   LLM support:
    -   Groq (LLM inference)
    -   HuggingFace (embeddings)
    -   Cohere (optional embeddings)

------------------------------------------------------------------------

## Tech Stack

-   Python 3.10+
-   Streamlit
-   LangChain
-   FAISS
-   HuggingFace Sentence Transformers
-   Groq LLM API

------------------------------------------------------------------------

## Folder Structure

    pdf-rag-chatbot/
    │
    ├── app.py
    ├── requirements.txt
    ├── README.md
    │
    ├── data/uploads/
    ├── vectorstore/faiss_index/
    │
    ├── src/
    │   ├── config.py
    │   ├── pdf_loader.py
    │   ├── vector_store.py
    │   └── rag_chain.py
    │
    └── .env

------------------------------------------------------------------------

## Environment Setup

### 1. Create Virtual Environment

``` bash
python -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

``` bash
pip install -r requirements.txt
```

### 3. API Keys (.env)

``` env
GROQ_API_KEY=your_groq_key
HUGGINGFACEHUB_API_TOKEN=your_hf_token
COHERE_API_KEY=your_cohere_key   # optional
```

------------------------------------------------------------------------

## requirements.txt

``` numpy==1.24.4
streamlit==1.31.1

langchain==0.1.16
langchain-community==0.0.34
langchain-core==0.1.53

langchain-groq==0.1.5
langchain-cohere==0.1.5

chromadb==0.4.24
pypdf==3.17.4

python-dotenv
tiktoken
huggingface-hub==0.20.3

```

##execute to launch streamlit application
streamlit run app.py

the above command launches webapplication , you can upload pdf file and prompt about the file.

## Learning Objectives

-   Understand RAG pipelines
-   Implement vector databases
-   Add conversational memory
-   Build LLM-powered UIs
-   Work with non-OpenAI providers

------------------------------------------------------------------------

## Next Improvements

-   Multi-PDF ingestion
-   Source citations
-   Persistent memory
-   User authentication
-   Chunk visualization

------------------------------------------------------------------------

Happy learning 🚀

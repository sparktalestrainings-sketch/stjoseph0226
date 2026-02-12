"""
utils/rag.py
FIXED VERSION - Compatible with LangChain 0.1.x
"""

import os
from pathlib import Path
from typing import List, Tuple, Optional

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

# ── Paths ─────────────────────────────────────────────────────────
UPLOAD_DIR = Path("uploads")
VECTOR_DIR = Path("vectorstore")
DATA_DIR = Path("data/sample_docs")

UPLOAD_DIR.mkdir(exist_ok=True)
VECTOR_DIR.mkdir(exist_ok=True)

# ── Splitter ──────────────────────────────────────────────────────
_splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=100,
    separators=["\n\n", "\n", ". ", "! ", "? ", " "],
)

# ── Healthcare Prompt ─────────────────────────────────────────────
HEALTHCARE_PROMPT_TEMPLATE = """You are MedAssist, a knowledgeable healthcare information assistant.

IMPORTANT RULES:
1. Answer ONLY using the context provided below
2. If information is not in the context, say: "I don't have specific information about that in my knowledge base"
3. Always add a disclaimer for medical advice
4. For emergencies, direct to emergency services
5. Never diagnose - provide information only

Context:
{context}

Chat History:
{chat_history}

Question: {question}

Answer:"""

# ── File Loaders ──────────────────────────────────────────────────
def load_file(path: str) -> List[Document]:
    """Load a single PDF or TXT file."""
    p = Path(path)
    try:
        if p.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(p))
        else:
            loader = TextLoader(str(p), encoding="utf-8")
        
        docs = loader.load()
        for doc in docs:
            doc.metadata["source_file"] = p.name
        return docs
    except Exception as e:
        print(f"⚠️  Could not load {path}: {e}")
        return []


def load_files(paths: List[str]) -> Tuple[List[Document], List[dict]]:
    """Load multiple files."""
    all_docs, meta = [], []
    for path in paths:
        docs = load_file(path)
        pages = len(docs)
        all_docs.extend(docs)
        meta.append({
            "filename": Path(path).name,
            "pages": pages,
            "path": path,
        })
    return all_docs, meta


# ── Vector Store ──────────────────────────────────────────────────
def _index_path(session_id: str) -> str:
    return str(VECTOR_DIR / f"idx_{session_id}")


def build_vectorstore(paths: List[str], embeddings, session_id: str = "default"):
    """Build FAISS vector store from files."""
    docs, meta = load_files(paths)
    if not docs:
        raise ValueError("No content extracted from files")
    
    chunks = _splitter.split_documents(docs)
    print(f"📄 Created {len(chunks)} chunks from {len(docs)} documents")
    
    vs = FAISS.from_documents(chunks, embeddings)
    vs.save_local(_index_path(session_id))
    return vs, meta


def add_to_vectorstore(existing: FAISS, paths: List[str], embeddings, session_id: str = "default"):
    """Add new documents to existing vector store."""
    docs, meta = load_files(paths)
    if docs:
        chunks = _splitter.split_documents(docs)
        existing.add_documents(chunks)
        existing.save_local(_index_path(session_id))
    return existing, meta


def load_vectorstore(embeddings, session_id: str = "default") -> Optional[FAISS]:
    """Load persisted FAISS index."""
    path = _index_path(session_id)
    if os.path.exists(path):
        return FAISS.load_local(
            path, 
            embeddings, 
            allow_dangerous_deserialization=True
        )
    return None


# ── RAG Chain ─────────────────────────────────────────────────────
def build_rag_chain(vectorstore: FAISS, llm, k: int = 5):
    """Build ConversationalRetrievalChain."""
    
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )
    
    # Use simple ConversationBufferMemory (more stable than WindowMemory)
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )
    
    # Build chain
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        verbose=False,
        combine_docs_chain_kwargs={
            "prompt": PromptTemplate(
                input_variables=["context", "question"],
                template=HEALTHCARE_PROMPT_TEMPLATE
            )
        }
    )
    
    return chain


# ── Utilities ─────────────────────────────────────────────────────
def save_uploaded_file(uploaded_file) -> str:
    """Save Streamlit UploadedFile to disk."""
    dest = UPLOAD_DIR / uploaded_file.name
    with open(dest, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return str(dest)


def format_sources(source_docs: List[Document]) -> str:
    """Format source documents into citations."""
    if not source_docs:
        return ""
    
    seen = set()
    lines = []
    for doc in source_docs:
        src = doc.metadata.get("source_file", "knowledge base")
        page = doc.metadata.get("page", "")
        key = f"{src}:{page}"
        
        if key not in seen:
            seen.add(key)
            pg_str = f" — page {page}" if page != "" else ""
            lines.append(f"📄 {src}{pg_str}")
    
    return "\n".join(lines)


def get_sample_doc_paths() -> List[str]:
    """Return paths to sample knowledge base documents."""
    if not DATA_DIR.exists():
        return []
    return [str(p) for p in DATA_DIR.glob("*.txt")] + \
           [str(p) for p in DATA_DIR.glob("*.pdf")]

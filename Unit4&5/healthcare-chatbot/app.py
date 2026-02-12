"""
app.py - MedAssist Healthcare AI (FIXED & STABLE)
Compatible with Python 3.10-3.11, LangChain 0.1.x
"""

import streamlit as st
import uuid
import os
from pathlib import Path

# Set page config FIRST before any other Streamlit commands
st.set_page_config(
    page_title="MedAssist Healthcare AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Now safe to import everything else
from utils.llm_provider import get_llm, get_embeddings, GROQ_MODELS, COHERE_MODELS
from utils.rag import (
    build_vectorstore, add_to_vectorstore, 
    build_rag_chain, save_uploaded_file, 
    format_sources, get_sample_doc_paths
)
from utils.logger import log_query, log_error

# ═══════════════════════════════════════════════════════════════════
# CSS STYLING
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp { background: #f5f7fa; }

/* Header */
.header-box {
    background: linear-gradient(135deg, #0d4f5c 0%, #1a7a8a 100%);
    padding: 24px;
    border-radius: 12px;
    color: white;
    margin-bottom: 24px;
}
.header-box h1 { margin: 0; font-size: 2rem; }
.header-box p { margin: 8px 0 0 0; opacity: 0.85; }

/* Stats */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 20px;
}
.stat-card {
    background: white;
    padding: 16px;
    border-radius: 8px;
    text-align: center;
    border: 1px solid #e0e0e0;
}
.stat-num { font-size: 1.8rem; font-weight: 700; color: #0d4f5c; }
.stat-lbl { font-size: 0.75rem; color: #666; text-transform: uppercase; }

/* Status */
.status { 
    padding: 10px 16px; 
    border-radius: 8px; 
    margin-bottom: 16px;
    font-size: 0.9rem;
}
.status-ready { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
.status-empty { background: #fff3cd; color: #856404; border: 1px solid #ffeaa7; }

/* Sources */
.sources {
    background: #f0f9fa;
    border-left: 3px solid #22a8be;
    padding: 12px;
    margin: 12px 0;
    border-radius: 4px;
    font-size: 0.85rem;
}

/* Emergency */
.emergency {
    background: #f8d7da;
    color: #721c24;
    padding: 12px;
    border-radius: 8px;
    border: 1px solid #f5c6cb;
    margin: 12px 0;
    font-weight: 600;
}

/* Disclaimer */
.disclaimer {
    background: #fff8e1;
    border: 1px solid #ffe082;
    padding: 10px;
    border-radius: 6px;
    font-size: 0.8rem;
    margin-top: 12px;
    color: #795548;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════════
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]
if "messages" not in st.session_state:
    st.session_state.messages = []
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "embeddings" not in st.session_state:
    st.session_state.embeddings = None
if "uploaded_docs" not in st.session_state:
    st.session_state.uploaded_docs = []
if "kb_loaded" not in st.session_state:
    st.session_state.kb_loaded = False

# ═══════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════
def get_api_key(provider: str) -> str:
    """Get API key from secrets or environment."""
    key_name = f"{provider}_api_key"
    try:
        # Try secrets.toml first
        if hasattr(st, 'secrets') and key_name in st.secrets:
            return st.secrets[key_name]
    except Exception:
        pass
    
    # Try environment variable
    env_key = "GROQ_API_KEY" if provider == "groq" else "COHERE_API_KEY"
    return os.getenv(env_key, "")

# ═══════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("# 🩺 MedAssist")
    st.markdown("*Healthcare AI Assistant*")
    st.markdown("---")
    
    # Provider selection
    provider = st.selectbox("🔌 Provider", ["groq", "cohere"], index=0)
    
    # API key input
    default_key = get_api_key(provider)
    api_key = st.text_input(
        f"API Key ({provider.capitalize()})",
        value=default_key,
        type="password",
        help=f"Get free key: {'console.groq.com' if provider == 'groq' else 'dashboard.cohere.com'}"
    )
    
    # Model selection
    models = GROQ_MODELS if provider == "groq" else COHERE_MODELS
    model = st.selectbox("Model", models, index=0)
    
    temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.05)
    
    st.markdown("---")
    st.markdown("### 📚 Knowledge Base")
    
    # Load built-in KB
    if not st.session_state.kb_loaded:
        if st.button("⚡ Load Medical KB", use_container_width=True):
            if not api_key:
                st.error("❌ Enter API key first")
            else:
                with st.spinner("Loading..."):
                    try:
                        # Initialize embeddings once
                        if st.session_state.embeddings is None:
                            st.session_state.embeddings = get_embeddings()
                        
                        # Get sample docs
                        paths = get_sample_doc_paths()
                        if not paths:
                            st.error("No sample docs found in data/sample_docs/")
                        else:
                            # Build vector store
                            vs, meta = build_vectorstore(
                                paths,
                                st.session_state.embeddings,
                                st.session_state.session_id
                            )
                            
                            # Build LLM and chain
                            llm = get_llm(provider, api_key, model, temperature)
                            chain = build_rag_chain(vs, llm)
                            
                            # Save to session
                            st.session_state.vectorstore = vs
                            st.session_state.rag_chain = chain
                            st.session_state.kb_loaded = True
                            st.session_state.uploaded_docs = meta
                            
                            st.success(f"✅ Loaded {len(paths)} documents!")
                            st.rerun()
                            
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        log_error(e, "KB load")
    
    # Upload PDFs
    st.markdown("#### Upload PDFs")
    uploaded = st.file_uploader(
        "Upload files",
        type=["pdf", "txt"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    
    if uploaded:
        if st.button("📥 Process", type="primary", use_container_width=True):
            if not api_key:
                st.error("❌ Enter API key first")
            else:
                with st.spinner("Processing..."):
                    try:
                        if st.session_state.embeddings is None:
                            st.session_state.embeddings = get_embeddings()
                        
                        # Save files
                        paths = [save_uploaded_file(f) for f in uploaded]
                        
                        # Build or update vector store
                        if st.session_state.vectorstore is None:
                            vs, meta = build_vectorstore(
                                paths,
                                st.session_state.embeddings,
                                st.session_state.session_id
                            )
                        else:
                            vs, meta = add_to_vectorstore(
                                st.session_state.vectorstore,
                                paths,
                                st.session_state.embeddings,
                                st.session_state.session_id
                            )
                        
                        # Build chain
                        llm = get_llm(provider, api_key, model, temperature)
                        chain = build_rag_chain(vs, llm)
                        
                        st.session_state.vectorstore = vs
                        st.session_state.rag_chain = chain
                        
                        # Update doc list
                        for m in meta:
                            if m["filename"] not in [d["filename"] for d in st.session_state.uploaded_docs]:
                                st.session_state.uploaded_docs.append(m)
                        
                        st.success(f"✅ Added {len(paths)} files!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        log_error(e, "Upload")
    
    # Show uploaded docs
    if st.session_state.uploaded_docs:
        st.markdown("**Documents:**")
        for doc in st.session_state.uploaded_docs:
            st.caption(f"📄 {doc['filename']} ({doc.get('pages', '?')} pages)")
    
    st.markdown("---")
    
    # Controls
    col1, col2 = st.columns(2)
    if col1.button("🗑️ Clear"):
        st.session_state.messages = []
        st.rerun()
    if col2.button("🔄 Reset"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    # Emergency
    st.markdown("---")
    st.markdown("""
    <div style='background:#f8d7da;padding:10px;border-radius:6px;font-size:0.8rem;'>
    <strong>🚨 Emergency</strong><br>
    National: 112<br>
    Ambulance: 108
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# MAIN AREA
# ═══════════════════════════════════════════════════════════════════

# Header
st.markdown("""
<div class="header-box">
    <h1>🩺 MedAssist Healthcare AI</h1>
    <p>Your intelligent medical information assistant powered by RAG</p>
</div>
""", unsafe_allow_html=True)

# Stats
total_pages = sum(d.get('pages', 0) for d in st.session_state.uploaded_docs)
st.markdown(f"""
<div class="stat-grid">
    <div class="stat-card">
        <div class="stat-num">{len(st.session_state.messages) // 2}</div>
        <div class="stat-lbl">Queries</div>
    </div>
    <div class="stat-card">
        <div class="stat-num">{len(st.session_state.uploaded_docs)}</div>
        <div class="stat-lbl">Documents</div>
    </div>
    <div class="stat-card">
        <div class="stat-num">{total_pages}</div>
        <div class="stat-lbl">Pages</div>
    </div>
    <div class="stat-card">
        <div class="stat-num">{provider.upper()}</div>
        <div class="stat-lbl">Provider</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Status
if st.session_state.rag_chain:
    st.markdown(
        f'<div class="status status-ready">✅ Ready — {len(st.session_state.uploaded_docs)} documents loaded</div>',
        unsafe_allow_html=True
    )
else:
    st.markdown(
        '<div class="status status-empty">⬆️ Load the Knowledge Base from sidebar to begin</div>',
        unsafe_allow_html=True
    )

# Quick questions
if st.session_state.rag_chain and not st.session_state.messages:
    st.markdown("**💡 Try asking:**")
    cols = st.columns(3)
    examples = [
        "What is the safe dose of paracetamol?",
        "How to perform CPR?",
        "Symptoms of diabetes?",
    ]
    for i, ex in enumerate(examples):
        if cols[i].button(ex, key=f"ex{i}"):
            st.session_state._pending = ex
            st.rerun()

# Chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("📎 Sources"):
                st.markdown(f'<div class="sources">{msg["sources"]}</div>', unsafe_allow_html=True)
        if msg["role"] == "assistant":
            st.markdown(
                '<div class="disclaimer">⚠️ For educational purposes. Consult a healthcare professional.</div>',
                unsafe_allow_html=True
            )

# Chat input
pending = st.session_state.pop("_pending", None)
user_input = st.chat_input(
    "Ask a medical question..." if st.session_state.rag_chain else "Load KB first...",
    disabled=not st.session_state.rag_chain
) or pending

if user_input and st.session_state.rag_chain:
    # Check for emergency keywords
    EMERGENCY_KW = ["chest pain", "can't breathe", "heart attack", "stroke", "emergency"]
    is_emergency = any(kw in user_input.lower() for kw in EMERGENCY_KW)
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Show emergency banner
    if is_emergency:
        st.markdown(
            '<div class="emergency">🚨 If life-threatening — CALL 112 or 108 NOW</div>',
            unsafe_allow_html=True
        )
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Searching..."):
            try:
                result = st.session_state.rag_chain({"question": user_input})
                answer = result.get("answer", str(result))
                sources = format_sources(result.get("source_documents", []))
            except Exception as e:
                answer = f"❌ Error: {str(e)}"
                sources = ""
                log_error(e, f"Query: {user_input}")
        
        st.markdown(answer)
        if sources:
            with st.expander("📎 Sources", expanded=True):
                st.markdown(f'<div class="sources">{sources}</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="disclaimer">⚠️ For educational purposes. Consult a healthcare professional.</div>',
            unsafe_allow_html=True
        )
    
    # Save to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources
    })
    
    log_query(user_input, answer, st.session_state.session_id, provider, model)
    st.rerun()

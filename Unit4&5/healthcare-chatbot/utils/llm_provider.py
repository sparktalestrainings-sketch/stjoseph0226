"""
utils/llm_provider.py
FIXED VERSION - Compatible with LangChain 0.1.x
"""

from typing import Literal

Provider = Literal["groq", "cohere"]

GROQ_MODELS = [
    "llama3-70b-8192",
    "llama3-8b-8192",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
    "llama-3.3-70b-versatile",
]

COHERE_MODELS = [
    "command-r-plus",
    "command-r",
    "command",
]


def get_llm(provider: Provider, api_key: str, model: str = None, temperature: float = 0.3):
    """Return a LangChain chat LLM for the given provider."""
    
    if provider == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(
            groq_api_key=api_key,
            model_name=model or "llama3-70b-8192",
            temperature=temperature,
        )
    
    elif provider == "cohere":
        from langchain_cohere import ChatCohere
        return ChatCohere(
            cohere_api_key=api_key,
            model=model or "command-r-plus",
            temperature=temperature,
        )
    
    else:
        raise ValueError(f"Unknown provider: {provider}")


def get_embeddings():
    """
    Local embeddings using sentence-transformers.
    Compatible with LangChain 0.1.x
    """
    from langchain_community.embeddings import HuggingFaceEmbeddings
    
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

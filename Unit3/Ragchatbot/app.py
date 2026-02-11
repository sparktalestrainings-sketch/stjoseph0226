
import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False"
os.environ["CHROMA_ANONYMIZED_TELEMETRY"] = "False"
import streamlit as st
import tempfile
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
#from langchain_community.embeddings import CohereEmbeddings
from langchain_cohere import CohereEmbeddings
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory


load_dotenv()

st.set_page_config(page_title="PDF RAG Chatbot", layout="wide")
st.title("📄 PDF Q&A Chatbot (RAG + Memory)")

# Session state
if "chain" not in st.session_state:
    st.session_state.chain = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Upload PDF
uploaded_pdf = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_pdf and st.button("Process PDF"):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_pdf.read())
        pdf_path = tmp.name

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    chunks = splitter.split_documents(documents)

    #embeddings = CohereEmbeddings(model="embed-english-v3.0")
    embeddings = CohereEmbeddings(
        model="embed-english-v3.0",
        cohere_api_key=os.getenv("COHERE_API_KEY")
    )

    #st.write("Cohere key loaded:", os.getenv("COHERE_API_KEY") is not None)


    vectordb = Chroma.from_documents(
        chunks,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )

    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    st.session_state.chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory
    )

    st.success("✅ PDF processed. Ask your questions below!")

# Chat UI
if st.session_state.chain:
    user_question = st.text_input("Ask a question about the PDF")

    if user_question:
        result = st.session_state.chain.invoke(
            {"question": user_question}
        )

        st.session_state.chat_history.append(
            ("You", user_question)
        )
        st.session_state.chat_history.append(
            ("Bot", result["answer"])
        )

    for role, message in st.session_state.chat_history:
        if role == "You":
            st.markdown(f"**🧑 {message}**")
        else:
            st.markdown(f"**🤖 {message}**")

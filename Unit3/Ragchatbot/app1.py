import os
import streamlit as st
from dotenv import load_dotenv

# Disable Chroma telemetry (optional)
os.environ["ANONYMIZED_TELEMETRY"] = "False"

load_dotenv()

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

from langchain_cohere import CohereEmbeddings
from langchain_groq import ChatGroq

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="PDF RAG Chatbot", layout="wide")
st.title("📄 PDF RAG Chatbot with Memory")

# -------------------------------
# API Keys check
# -------------------------------
if not os.getenv("COHERE_API_KEY"):
    st.error("COHERE_API_KEY not found in environment variables")
    st.stop()

if not os.getenv("GROQ_API_KEY"):
    st.error("GROQ_API_KEY not found in environment variables")
    st.stop()

# -------------------------------
# File Upload
# -------------------------------
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    if st.button("Process PDF"):
        with st.spinner("Processing PDF..."):

            # Load PDF
            loader = PyPDFLoader("temp.pdf")
            documents = loader.load()

            # Split text
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            chunks = splitter.split_documents(documents)

            # Embeddings
            embeddings = CohereEmbeddings(
                model="embed-english-v3.0",
                cohere_api_key=os.getenv("COHERE_API_KEY")
            )

            # Vector Store
            vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=embeddings
            )

            # LLM
            llm = ChatGroq(
                model="llama3-8b-8192",
                groq_api_key=os.getenv("GROQ_API_KEY"),
                temperature=0
            )

            # Memory (IMPORTANT)
            memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )

            # RAG Chain
            st.session_state.qa_chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=vectorstore.as_retriever(),
                memory=memory,
                return_source_documents=True
            )

            st.success("PDF processed. Ask your questions below!")

# -------------------------------
# Question Answering
# -------------------------------
if "qa_chain" in st.session_state:
    user_question = st.text_input("Ask a question")

    if user_question:
        response = st.session_state.qa_chain(
            {"question": user_question}
        )

        st.subheader("Answer")
        st.write(response["answer"])

# 📈 Stock Market LLM Chatbot

### FastAPI + LangServe + Groq + Streamlit (Full Stack)

------------------------------------------------------------------------

## 🚀 Project Overview

This project is a Full-Stack LLM-based Stock Market Chatbot built using:

-   FastAPI (Backend API)
-   LangServe (LLM route management)
-   Groq LLM (Llama3 model)
-   Streamlit (Frontend UI)
-   Stock Price Logic (API-based or demo logic)

------------------------------------------------------------------------

## 🏗 Architecture

Streamlit Frontend\
↓\
FastAPI Backend\
↓\
LangServe Chain\
↓\
Groq LLM + Stock API Logic

------------------------------------------------------------------------

## 📁 Folder Structure

stock-llm-chatbot/ 
│ ├── backend/ 
│ ├── app.py 
│ └── requirements.txt 
│
├── frontend/ 
│ ├── app.py 
│ └── requirements.txt 
│ 
└── README.md
│ 
└── .env

------------------------------------------------------------------------

## 🧑‍💻 Step 1: Create Virtual Environment

python -m venv venv

Activate:

Windows: .\venv\scritps\activate



------------------------------------------------------------------------

## 📦 Step 2: Install Backend Dependencies

pip install -r .\backend\requirements.txt

------------------------------------------------------------------------

## 📦 Step 3: Install Frontend Dependencies

pip install -r .\frontend\requirements.txt

------------------------------------------------------------------------

## ▶ Step 4: update api key

open .env file , update your keys 
GROQ_API_KEY
STOCK_API_KEY
    https://www.alphavantage.co/
    https://www.alphavantage.co/support/#api-key

------------------------------------------------------------------------
## ▶ Step 5: Run Backend
cd backend
uvicorn app:app --reload --port 8000

Visit: http://localhost:8000/docs

------------------------------------------------------------------------

## ▶ Step 6: Run Frontend

cd frontend > streamlit run app.py

------------------------------------------------------------------------


## 🧪 Sample Prompts

Stock Price: - What is price of AAPL? - Tell me the price of TSLA -
Current price of MSFT

General LLM: - Explain stock market. - What is a bull market? - Explain
P/E ratio.

------------------------------------------------------------------------

## 🔎 API Endpoints

-   POST /chat/invoke
-   POST /chat/stream
-   GET /chat/playground/
-   GET /docs

------------------------------------------------------------------------

## 🎯 Features

-   Full Stack Architecture
-   LLM Integration
-   Stock API Logic
-   FastAPI Backend
-   Streamlit Chat UI
-   LangServe Ready

------------------------------------------------------------------------

## 🧠 Technologies Used

-   Python 3.10+
-   FastAPI
-   LangChain
-   LangServe
-   Groq LLM
-   Streamlit

------------------------------------------------------------------------

## 📌 Future Enhancements

-   Authentication
-   PostgreSQL logging
-   Real stock API integration
-   Docker deployment

------------------------------------------------------------------------

Developed for academic and real-world full-stack LLM integration
practice.

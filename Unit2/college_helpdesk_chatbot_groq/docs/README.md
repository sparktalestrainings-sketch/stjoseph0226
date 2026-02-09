# 🎓 College Helpdesk Chatbot (Groq)

An AI-powered **College Helpdesk Chatbot** built using **Python, Streamlit, and Groq LLMs**, implementing **role-based prompting**, **multi-turn dialogue**, and **grounded responses** to avoid hallucinations.

This project is suitable for **mini projects, final-year projects**, and **AI demonstrations**.

---

## 📌 Features

- ✅ Role-Based Prompting (Academic, Admissions, Finance, IT)
- ✅ Multi-Turn Dialogue with Context Memory
- ✅ Intent Classification
- ✅ Groq LLaMA-3 Integration
- ✅ Hallucination Prevention using Grounded Academic Policy
- ✅ Streamlit Web Interface
- ✅ Modular and Viva-Friendly Code Structure

---

## 🧠 Key Concepts Used

- Conversational AI
- Role-Based Prompt Engineering
- Multi-Turn Dialogue Management
- Context Persistence
- Grounded Generation (RAG-lite)
- Large Language Models (LLMs)

---

## 🏗️ Project Architecture

User
↓
Streamlit UI
↓
Intent Classifier
↓
Memory Manager
↓
Role-Based Prompt Generator
↓
Academic Policy Injection (Grounded Data)
↓
Groq LLM (LLaMA-3)
↓
Response



---

## 📁 Folder Structure

ollege_helpdesk_chatbot/
│
├── app/
│ ├── main.py
│ └── utils/
│ ├── intent.py
│ ├── prompts.py
│ └── memory.py
│
├── data/
│ └── academic_policy.json
│
├── docs/
│ └── README.md
│
├── requirements.txt
└── README.md



---

## ⚙️ Technologies Used

| Component | Technology |
|--------|------------|
| Frontend | Streamlit |
| Backend | Python |
| LLM | Groq (LLaMA-3) |
| Memory | Streamlit Session State |
| Prompting | Role-Based Prompt Engineering |
| Data | JSON (Academic Policy) |

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/college-helpdesk-chatbot-groq.git
cd college-helpdesk-chatbot-groq

##Install Dependencies
pip install -r requirements.txt

##Run the Application
streamlit run app/main.py


Enter Groq API Key
Paste your Groq API key in the sidebar input
The key is not stored (secure for demos & exams)

💬 Sample Queries to Test

What is the course registration deadline?
What about late registration?
How do I register for courses?
What is the admission process?


🧠 How Multi-Turn Dialogue Works

The chatbot stores:
Last detected intent
Intent history
Last user query
This allows follow-up questions like:
“What about late registration?”
to be answered correctly without repeating context.


🛡️ Hallucination Prevention

To prevent the LLM from inventing facts:
All academic rules are stored in academic_policy.json
Policies are injected into the system prompt
The model is instructed:
❌ Do not guess
❌ Do not invent universities or dates
✅ Use only official policy data
This technique is known as Grounded Generation (RAG-lite).


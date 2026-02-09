import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

from utils.intent import detect_intent
from utils.prompts import get_system_prompt
from utils.memory import init_memory, update_memory

# ---------------- Streamlit Config ----------------
st.set_page_config(page_title="College Helpdesk Chatbot")
st.title("🎓 College Helpdesk Chatbot (Groq)")

# ---------------- Sidebar ----------------
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter Groq API Key", type="password")

if not api_key:
    st.warning("Please enter your Groq API key to continue.")

client = Groq(api_key=api_key) if api_key else None

# ---------------- Session State ----------------
if "memory" not in st.session_state:
    st.session_state.memory = init_memory()

if "chat" not in st.session_state:
    st.session_state.chat = []

# ---------------- Chat Input ----------------
user_input = st.text_input("Ask your question")

if st.button("Send") and user_input and client:
    # intent = detect_intent(user_input)
    #system_prompt = get_system_prompt(intent)
    detected_intent = detect_intent(user_input)
    # If intent is general but we already have context, reuse last intent
    if detected_intent == "general" and st.session_state.memory["active_intent"]:
        intent = st.session_state.memory["active_intent"]
    else:
        intent = detected_intent
    system_prompt = get_system_prompt(intent)

    
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "assistant",
            "content": f"Conversation context: {st.session_state.memory}"
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.4,
        max_tokens=300
    )

    bot_reply = response.choices[0].message.content

    st.session_state.chat.append(("User", user_input))
    st.session_state.chat.append(("Bot", bot_reply))

    update_memory(st.session_state.memory, intent, user_input)

# ---------------- Display Chat ----------------
for role, msg in st.session_state.chat:
    st.markdown(f"**{role}:** {msg}")

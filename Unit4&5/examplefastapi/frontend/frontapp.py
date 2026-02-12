import streamlit as st
import requests

st.title("📈 Stock Market LLM Chatbot")

api_key = st.sidebar.text_input("Enter Groq API Key", type="password")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Ask something...")

if user_input and api_key:
    response = requests.post(
        "http://localhost:8000/chat/invoke",
        json={
            "input": {
                "message": user_input,
                "api_key": api_key
            }
        }
    )

    result = response.json()
    reply = result["output"]

    st.session_state.messages.append(("You", user_input))
    st.session_state.messages.append(("Bot", reply))

for role, msg in st.session_state.messages:
    with st.chat_message("user" if role == "You" else "assistant"):
        st.write(msg)

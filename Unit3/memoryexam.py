from openai import OpenAI
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

conversation = [
    {"role": "system", "content": "You are a helpful tutor."}
]

while True:
    user_input = input("User: ")
    conversation.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=conversation,
        temperature=0.4
    )

    reply = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": reply})
    print("Bot:", reply)

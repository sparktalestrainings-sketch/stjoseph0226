import os
from dotenv import load_dotenv
from groq import Groq
from openai import OpenAI
load_dotenv()
#client = Groq(api_key="GROQ_API_KEY")
client = OpenAI(
    base_url="https://api.groq.com/openai/v1", # Point to Groq
    api_key=os.getenv("GROQ_API_KEY")
)
msgs = [
    {"role": "user", "content": "Q: What is AI? A: AI is the ability of machines to think like humans."},
    {"role": "user", "content": "Q: What is ML? A:"}
]

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=msgs,
    temperature=0.2
)

print(response.choices[0].message.content)

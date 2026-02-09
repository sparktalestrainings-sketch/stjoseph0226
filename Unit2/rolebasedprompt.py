import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

msgs = [
    {"role": "system", "content": "You are an HR interviewer."},
    {"role": "user", "content": "Ask me Python interview questions"}
]

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=msgs,
    temperature=0.2
)

print(response.choices[0].message.content)

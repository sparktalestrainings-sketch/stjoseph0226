import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
msgs = [
    {"role": "system", "content": "You are a math tutor."},
    {"role": "user", "content": "Explain recursion"},
    {"role": "assistant", "content": "Recursion is when a function calls itself."},
    {"role": "user", "content": "Give an example"}
]
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=msgs,
    temperature=0.2
)
print(response.choices[0].message.content)

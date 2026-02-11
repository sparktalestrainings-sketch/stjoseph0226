import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

context = "AI is used in chatbots to simulate conversation."
question = "How is AI used in chatbots?"

prompt = f"Answer using only this context:\n{context}\n\nQuestion: {question}"

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.2
)

print(response.choices[0].message.content)

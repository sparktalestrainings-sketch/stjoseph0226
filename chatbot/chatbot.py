import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = OpenAI(
    base_url="https://api.groq.com/openai/v1", # Point to Groq
    api_key=os.getenv("GROQ_API_KEY")
)


def get_response(messages):
    response = client.chat.completions.create(
        model= "llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content
'''
# List all active models to see current IDs
models = client.models.list()
for model in models.data:
    print(model.id)
'''

#pip install faiss-cpu

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv("HF_TOKEN"))

model = SentenceTransformer('all-MiniLM-L6-v2')

docs = [
    "AI is the simulation of human intelligence",
    "Python is a programming language",
    "Chatbots use natural language processing"
]

embeddings = model.encode(docs)
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))

query = model.encode(["What is a chatbot?"])
D, I = index.search(query, 1)
print(docs[I[0][0]])

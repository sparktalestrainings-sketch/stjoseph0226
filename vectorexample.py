import numpy as np

# Step 1: Define a tiny vocabulary
vocab = {
    "apple": 0,
    "banana": 1,
    "car": 2,
    "bus": 3
}

vocab_size = len(vocab)
embedding_dim = 5  # small for learning

# Step 2: Create an embedding matrix (randomly initialized)
embedding_matrix = np.random.rand(vocab_size, embedding_dim)

# Step 3: Function to get embedding for a word
def get_embedding(word):
    idx = vocab[word]
    return embedding_matrix[idx]

# Test
print("Embedding for 'apple':", get_embedding("apple"))
print("Embedding for 'banana':", get_embedding("banana"))
'''
What this teaches

Each word → vector

Embedding matrix shape = vocab_size × embedding_dim

Similar words can become similar vectors after training
'''




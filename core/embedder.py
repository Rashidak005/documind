import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL

# Load the embedding model once at module level
# This means it loads into memory when this file is imported
# and stays loaded for the entire session — no reloading on every call
model = SentenceTransformer(EMBEDDING_MODEL)

# --- Generate Embeddings for a List of Chunks ---

def embed_chunks(chunks):

    print(f"Generating embeddings for {len(chunks)} chunks...")

    # Encode all chunks at once — faster than one by one
    embeddings = model.encode(chunks, show_progress_bar=True)

    print(f"Generated {len(embeddings)} embeddings of size {embeddings[0].shape[0]}")

    # Convert numpy arrays to plain Python lists for ChromaDB
    return embeddings.tolist()

# --- Generate Embedding for a Single Query ---

def embed_query(query):
    embedding = model.encode(query)
    return embedding.tolist()


# --- Quick Test ---

if __name__ == "__main__":

    test_chunks = [
        "Artificial neural networks are inspired by the human brain.",
        "The perceptron is the simplest form of a neural network.",
        "ReLU is one of the most commonly used activation functions."
    ]

    embeddings = embed_chunks(test_chunks)

    print(f"\nNumber of embeddings: {len(embeddings)}")
    print(f"Embedding size: {len(embeddings[0])}")
    print(f"First 5 values of first embedding: {embeddings[0][:5]}")
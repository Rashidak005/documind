import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chromadb
from config import CHROMA_PATH, TOP_K_RESULTS
from core.embedder import embed_chunks, embed_query

# Initialize ChromaDB persistent client
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

# --- Get or Create a Collection for a Specific Document ---

def get_collection(collection_name):
    return chroma_client.get_or_create_collection(name=collection_name)

# --- Store Chunks in ChromaDB ---

def store_chunks(chunks, collection_name):

    collection = get_collection(collection_name)

    # Check if this document was already stored before
    existing = collection.count()
    if existing > 0:
        print(f"Collection '{collection_name}' already has {existing} chunks. Clearing and re-storing...")
        chroma_client.delete_collection(name=collection_name)
        collection = get_collection(collection_name)

    # Generate embeddings for all chunks
    embeddings = embed_chunks(chunks)

    # Create unique IDs for each chunk
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    # Store everything in ChromaDB
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids
    )

    print(f"Stored {len(chunks)} chunks in collection '{collection_name}'")
    return len(chunks)

# --- Search for Relevant Chunks ---

def search_chunks(query, collection_name, top_k=TOP_K_RESULTS):

    collection = get_collection(collection_name)

    # Check collection is not empty
    if collection.count() == 0:
        raise ValueError(f"Collection '{collection_name}' is empty. Please upload a document first.")

    # Embed the query
    query_embedding = embed_query(query)

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count())
    )

    # Return chunks and their similarity distances
    chunks = results["documents"][0]
    distances = results["distances"][0]

    return chunks, distances

# --- List All Collections ---

def list_collections():
    collections = chroma_client.list_collections()
    return [col.name for col in collections]

# --- Delete a Collection ---

def delete_collection(collection_name):
    chroma_client.delete_collection(name=collection_name)
    print(f"Deleted collection '{collection_name}'")


# --- Quick Test ---

if __name__ == "__main__":

    from core.loader import load_document
    from core.chunker import chunk_text

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pdf_path = os.path.join(BASE_DIR, "yourfile.pdf")

    text = load_document(pdf_path)
    chunks = chunk_text(text)

    store_chunks(chunks, "test_collection")

    print("\n--- Testing Search ---")
    results, distances = search_chunks("what is a perceptron", "test_collection")

    for i, (chunk, distance) in enumerate(zip(results, distances)):
        print(f"\nResult {i+1} (distance: {distance:.4f}):")
        print(chunk[:200])
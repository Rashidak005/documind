import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.loader import load_document
from core.chunker import chunk_text
from core.vector_store import store_chunks, search_chunks, list_collections
from core.generator import generate_answer, generate_summary
from config import UPLOAD_PATH

import shutil

# --- Process and Store an Uploaded Document ---

def process_document(file_path, file_name):

    print(f"\n=== Processing: {file_name} ===")

    # Step 1 - Load text from document
    text = load_document(file_path)

    # Step 2 - Chunk the text
    chunks = chunk_text(text)

    # Step 3 - Create a clean collection name from filename
    # Remove extension and replace spaces/special chars with underscores
    collection_name = os.path.splitext(file_name)[0]
    collection_name = "".join(c if c.isalnum() else "_" for c in collection_name).lower()

    # Step 4 - Store chunks in ChromaDB
    store_chunks(chunks, collection_name)

    # Step 5 - Generate a summary of the document
    summary = generate_summary(chunks)

    print(f"=== Document '{file_name}' processed successfully ===\n")

    return {
        "file_name": file_name,
        "collection_name": collection_name,
        "chunk_count": len(chunks),
        "character_count": len(text),
        "summary": summary
    }

# --- Ask a Question About a Document ---

def ask_question(query, collection_name):

    if not query.strip():
        return "Please enter a question."

    # Retrieve relevant chunks
    chunks, distances = search_chunks(query, collection_name)

    # Generate answer from those chunks
    answer = generate_answer(query, chunks, distances)

    return answer

# --- Get All Available Documents ---

def get_available_documents():
    return list_collections()


# --- Quick Test ---

if __name__ == "__main__":

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pdf_path = os.path.join(BASE_DIR, "yourfile.pdf")

    # Process the document
    result = process_document(pdf_path, "yourfile.pdf")

    print("Document Info:")
    print(f"  File: {result['file_name']}")
    print(f"  Chunks: {result['chunk_count']}")
    print(f"  Characters: {result['character_count']}")
    print(f"\nAuto Summary:\n{result['summary']}")

    print("\n--- Testing Q&A ---")
    answer = ask_question(
        "What is the perceptron learning rule?",
        result["collection_name"]
    )
    print(f"\nAnswer: {answer}")
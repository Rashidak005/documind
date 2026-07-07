import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.loader import load_document
from core.chunker import chunk_text
from core.vector_store import store_chunks, search_chunks, list_collections, delete_collection
from core.generator import generate_answer, generate_summary, generate_multi_source_answer
from config import UPLOAD_PATH

import shutil

# --- Process and Store an Uploaded Document ---

def process_document(file_path, file_name):

    print(f"\n=== Processing: {file_name} ===")

    text = load_document(file_path)
    chunks = chunk_text(text)

    collection_name = os.path.splitext(file_name)[0]
    collection_name = "".join(c if c.isalnum() else "_" for c in collection_name).lower()

    store_chunks(chunks, collection_name)

    summary = generate_summary(chunks)

    print(f"=== Document '{file_name}' processed successfully ===\n")

    return {
        "file_name": file_name,
        "collection_name": collection_name,
        "chunk_count": len(chunks),
        "character_count": len(text),
        "summary": summary
    }


# --- Ask a Question About a Single Document ---

def ask_question(query, collection_name):

    if not query.strip():
        return "Please enter a question."

    chunks, distances = search_chunks(query, collection_name)
    answer = generate_answer(query, chunks, distances)

    return answer


# --- Ask a Question Across Multiple Documents ---

def ask_multiple_documents(query, collection_names, top_k_per_doc=3):
    """
    Searches across several document collections at once, combines the
    most relevant chunks from each (tagged with their source document),
    and generates one answer that can reference multiple documents.

    Returns a tuple: (answer_text, chunks_with_sources)
    """

    if not query.strip():
        return "Please enter a question.", []

    if not collection_names:
        return "Please select at least one document.", []

    all_chunks_with_sources = []

    for collection_name in collection_names:
        try:
            chunks, distances = search_chunks(query, collection_name, top_k=top_k_per_doc)
            for chunk in chunks:
                all_chunks_with_sources.append({
                    "text": chunk,
                    "source": collection_name
                })
        except ValueError:
            # Collection might be empty or missing — skip it, don't crash the whole search
            continue

    if not all_chunks_with_sources:
        return "No relevant information found in the selected documents.", []

    answer = generate_multi_source_answer(query, all_chunks_with_sources)
    return answer, all_chunks_with_sources


# --- Get All Available Documents ---

def get_available_documents():
    return list_collections()


# --- Quick Test ---

if __name__ == "__main__":

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pdf_path = os.path.join(BASE_DIR, "yourfile.pdf")

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
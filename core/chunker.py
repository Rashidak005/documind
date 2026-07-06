import os
import sys

# Add the parent DocuMind/ folder to Python's path
# so we can import config.py which lives there
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP

# --- Main Chunking Function ---

def chunk_text(text, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = splitter.split_text(text)

    # Filter out any chunks that are too short to be meaningful
    chunks = [chunk for chunk in chunks if len(chunk.strip()) > 50]

    print(f"Created {len(chunks)} chunks from {len(text)} characters")

    return chunks


# --- Quick Test ---

if __name__ == "__main__":

    from core.loader import load_document

    if len(sys.argv) < 2:
        print("Usage: python chunker.py <path_to_file>")
    else:
        file_path = sys.argv[1]

        # Load the document first
        text = load_document(file_path)

        # Then chunk it
        chunks = chunk_text(text)

        print(f"\n--- First Chunk ---\n{chunks[0]}")
        print(f"\n--- Last Chunk ---\n{chunks[-1]}")
        print(f"\n--- Chunk Size Range ---")
        sizes = [len(c) for c in chunks]
        print(f"Smallest chunk: {min(sizes)} characters")
        print(f"Largest chunk: {max(sizes)} characters")
        print(f"Average chunk: {sum(sizes) // len(sizes)} characters")
import re


def format_document_info(doc_info):
    """
    Takes the dictionary returned by pipeline.process_document()
    and formats it into a clean markdown string for display.
    """

    formatted = f"""### 📄 {doc_info['file_name']}

**Chunks:** {doc_info['chunk_count']}  
**Characters:** {doc_info['character_count']:,}

**Summary:**  
{doc_info['summary']}
"""

    return formatted


def format_answer(answer_text):
    """
    Cleans up the raw answer string from generator.generate_answer()
    and makes source citations like [Source 1] bold for display.
    """

    cleaned = answer_text.strip()
    formatted = re.sub(r"(\[Source \d+\])", r"**\1**", cleaned)

    return formatted


def format_multi_source_answer(answer_text, chunks_with_sources):
    """
    Takes the raw answer and the list of {"text": ..., "source": ...} chunks
    that were retrieved, and appends a clear "Sources" footer listing every
    document that was searched and contributed context — guaranteed to show,
    regardless of whether the model mentioned it in the answer itself.
    """

    cleaned = format_answer(answer_text)

    # Get unique document names, in the order they first appeared
    seen = []
    for item in chunks_with_sources:
        if item["source"] not in seen:
            seen.append(item["source"])

    if seen:
        sources_footer = "\n\n---\n📄 **Sources searched:** " + ", ".join(seen)
        return cleaned + sources_footer

    return cleaned


def format_document_list(collection_names):
    """
    Takes a list of collection names and formats it into a clean
    markdown bullet list.
    """

    if not collection_names:
        return "*No documents uploaded yet. Upload a document to get started.*"

    lines = []
    for name in collection_names:
        lines.append(f"- {name}")

    formatted = "\n".join(lines)

    return formatted


def format_error(error_message):
    """
    Wraps an error message in a consistent markdown format so it's
    clearly visible to the user in the Gradio interface.
    """

    return f"⚠️ **Error:** {error_message}"


# --- Quick Test ---
if __name__ == "__main__":

    test_doc_info = {
        "file_name": "yourfile.pdf",
        "collection_name": "yourfile",
        "chunk_count": 35,
        "character_count": 12947,
        "summary": "This document is about an Artificial Neural Networks (ANN) lab covering perceptrons and activation functions."
    }
    print("--- format_document_info ---")
    print(format_document_info(test_doc_info))

    test_answer = "The perceptron learning rule updates weights based on error. [Source 1]"
    print("--- format_answer ---")
    print(format_answer(test_answer))

    test_multi_chunks = [
        {"text": "chunk 1", "source": "lecture_notes"},
        {"text": "chunk 2", "source": "research_paper"},
        {"text": "chunk 3", "source": "lecture_notes"},
    ]
    print("--- format_multi_source_answer ---")
    print(format_multi_source_answer("Combined answer here. [Source 1]", test_multi_chunks))

    print("\n--- format_document_list (with items) ---")
    print(format_document_list(["yourfile", "lecture_notes", "research_paper"]))

    print("\n--- format_document_list (empty) ---")
    print(format_document_list([]))

    print("\n--- format_error ---")
    print(format_error("Unsupported file type: .exe"))
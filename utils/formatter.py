import re


def format_document_info(doc_info):
    """
    Takes the dictionary returned by pipeline.process_document()
    and formats it into a clean markdown string for display.

    Expected keys in doc_info:
    file_name, collection_name, chunk_count, character_count, summary
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

    Example: "The perceptron works this way. [Source 1]"
    becomes:  "The perceptron works this way. **[Source 1]**"
    """

    # Remove any extra leading/trailing whitespace
    cleaned = answer_text.strip()

    # Use regex to find patterns like [Source 1], [Source 12], etc.
    # and wrap them in ** ** so markdown renders them bold
    formatted = re.sub(r"(\[Source \d+\])", r"**\1**", cleaned)

    return formatted


def format_document_list(collection_names):
    """
    Takes a list of collection names (from pipeline.get_available_documents())
    and formats it into a clean markdown bullet list.

    Returns a friendly message if no documents have been uploaded yet.
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
    clearly visible to the user in the Gradio interface, instead of
    showing a raw Python exception.
    """

    return f"⚠️ **Error:** {error_message}"


# --- Quick Test ---
if __name__ == "__main__":

    # Test format_document_info
    test_doc_info = {
        "file_name": "yourfile.pdf",
        "collection_name": "yourfile",
        "chunk_count": 35,
        "character_count": 12947,
        "summary": "This document is about an Artificial Neural Networks (ANN) lab covering perceptrons and activation functions."
    }
    print("--- format_document_info ---")
    print(format_document_info(test_doc_info))

    # Test format_answer
    test_answer = "The perceptron learning rule updates weights based on error. [Source 1]"
    print("--- format_answer ---")
    print(format_answer(test_answer))

    # Test format_document_list with items
    print("\n--- format_document_list (with items) ---")
    print(format_document_list(["yourfile", "lecture_notes", "research_paper"]))

    # Test format_document_list with empty list
    print("\n--- format_document_list (empty) ---")
    print(format_document_list([]))

    # Test format_error
    print("\n--- format_error ---")
    print(format_error("Unsupported file type: .exe"))
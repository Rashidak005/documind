import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME

client = Groq(api_key=GROQ_API_KEY)

# --- Generate Answer From Retrieved Chunks ---

def generate_answer(query, chunks, distances=None):

    # Format chunks into a numbered context block
    context_parts = []
    for i, chunk in enumerate(chunks):
        context_parts.append(f"[Source {i+1}]\n{chunk}")

    context = "\n\n".join(context_parts)

    # Build the prompt
    prompt = f"""You are DocuMind, an intelligent document assistant. 
Your job is to answer questions accurately using ONLY the provided document context.

Rules you must follow:
- Answer using ONLY information from the context below
- If the answer is not in the context, say exactly: "I could not find this information in the uploaded document."
- Always mention which source number your answer comes from
- Be concise but complete
- Do not use any outside knowledge or make assumptions

Document Context:
{context}

User Question: {query}

Answer:"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are DocuMind, a precise document question-answering assistant. You only answer from provided context and always cite your sources."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1
    )

    return response.choices[0].message.content


# --- Generate a Summary of the Document ---

def generate_summary(chunks):

    # Take the first 5 chunks for summarization
    sample_text = "\n\n".join(chunks[:5])

    prompt = f"""Based on the following document excerpts, provide a brief 3-4 sentence summary of what this document is about.

Document excerpts:
{sample_text}

Summary:"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


# --- Quick Test ---

if __name__ == "__main__":

    test_chunks = [
        "[Source 1]\nThe perceptron is the simplest neural network unit. It takes inputs, multiplies them by weights, sums them up, and passes the result through an activation function.",
        "[Source 2]\nActivation functions like ReLU, sigmoid, and tanh introduce non-linearity into neural networks, allowing them to learn complex patterns.",
        "[Source 3]\nThe perceptron learning rule updates weights based on the error between predicted and actual output."
    ]

    answer = generate_answer("How does a perceptron work?", test_chunks)
    print("Answer:", answer)
---
title: DocuMind
emoji: 🧠
colorFrom: purple
colorTo: blue
sdk: gradio
sdk_version: 6.19.0
app_file: app.py
pinned: false
---

# DocuMind

RAG-powered document Q&A app — upload a PDF, DOCX, TXT, or image and ask questions grounded entirely in that document's content, with every answer citing its source.

## How it works

1. **Upload** a document (PDF, DOCX, TXT, or PNG/JPG via OCR)
2. **Chunking** — the document is split into overlapping text chunks
3. **Embedding** — each chunk is converted into a vector using `sentence-transformers`
4. **Storage** — vectors are stored in a per-document ChromaDB collection
5. **Retrieval** — your question is embedded and matched against the most relevant chunks
6. **Generation** — Groq's Llama 3.3 model generates an answer using only the retrieved context, citing which source chunk it came from

## Tech Stack

| Component | Technology |
|---|---|
| LLM | Groq (Llama 3.3 70B) |
| Vector Database | ChromaDB |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Chunking | LangChain RecursiveCharacterTextSplitter |
| OCR | Tesseract |
| Frontend | Gradio |

## Running Locally

```bash
git clone https://github.com/Rashidak005/documind.git
cd documind
pip install -r requirements.txt
```

Create a `.env` file (see `.env.example`) with your Groq API key:
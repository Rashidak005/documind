import os
from dotenv import load_dotenv

# Find the root folder of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load environment variables
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

# --- API Settings ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama-3.3-70b-versatile"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# --- RAG Settings ---
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K_RESULTS = 4

# --- Storage Paths ---
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")
UPLOAD_PATH = os.path.join(BASE_DIR, "uploaded_docs")

# --- Supported File Types ---
SUPPORTED_EXTENSIONS = [".pdf", ".txt", ".docx", ".png", ".jpg", ".jpeg"]

# Create storage folders if they don't exist yet
os.makedirs(CHROMA_PATH, exist_ok=True)
os.makedirs(UPLOAD_PATH, exist_ok=True)
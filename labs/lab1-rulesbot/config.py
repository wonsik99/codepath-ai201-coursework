import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# --- LLM ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = "llama-3.3-70b-versatile"

# --- Embeddings ---
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# --- Vector store ---
CHROMA_COLLECTION = "rulesbot"
CHROMA_PATH = str(BASE_DIR / "chroma_db")

# --- Retrieval ---
N_RESULTS = 3
MAX_CONTEXT_DISTANCE = 0.55

# --- Documents ---
DOCS_PATH = str(BASE_DIR / "docs")

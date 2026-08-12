import os
from dotenv import load_dotenv

load_dotenv()

# --- LLM provider ---
# Set LLM_PROVIDER to "groq" or "openai" in .env
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")

if LLM_PROVIDER == "openai":
    LLM_MODEL = OPENAI_MODEL
elif LLM_PROVIDER == "groq":
    LLM_MODEL = GROQ_MODEL
else:
    raise ValueError(
        f"Invalid LLM_PROVIDER: {LLM_PROVIDER!r}. Use 'groq' or 'openai'."
    )

# --- Classifier ---
VALID_LABELS = ["interview", "solo", "panel", "narrative"]

# --- Data ---
DATA_PATH = "./data"
TRAIN_FILE = "train_episodes.json"
TEST_FILE = "test_episodes.json"
LABELS_FILE = "my_labels.json"

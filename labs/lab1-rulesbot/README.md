# 🎲 RulesBot

> A board game rules assistant — because "just read the rulebook" isn't always helpful at 11pm on game night.

RulesBot answers natural language questions about board game rules using a RAG
(Retrieval-Augmented Generation) pipeline. It retrieves relevant rule passages,
filters weak matches, and asks Groq to generate an answer grounded in the actual
text with game-name citations.

---

## Getting Started

### 1. Open the lab directory

From the consolidated coursework repository:

```bash
cd labs/lab1-rulesbot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # Mac/Linux
# or: .venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** `sentence-transformers` will download the embedding model (~80MB) on first run. This only happens once — it's cached locally afterward.

### 4. Add your Groq API key

```bash
cp .env.example .env
```

Open `.env` and replace `your_key_here` with your key from [console.groq.com](https://console.groq.com). No credit card required.

### 5. Run the app

```bash
python app.py
```

RulesBot starts locally and prints its browser URL. The first run downloads the
local embedding model and stores 149 rule chunks in `chroma_db/`; later runs
reuse that index.

---

## Project Structure

```
lab1-rulesbot/
├── app.py              # Gradio UI and startup logic — fully built
├── config.py           # Settings (models, paths, retrieval params) — fully built
├── ingest.py           # Document loading + overlapping character chunking
├── retriever.py        # Lazy ChromaDB setup, ingestion, and semantic search
├── generator.py        # Relevance filtering and grounded Groq generation
├── docs/               # Board game rule documents (pre-loaded)
│   ├── catan.txt
│   ├── clue.txt
│   ├── codenames.txt
│   ├── monopoly.txt
│   ├── pandemic.txt
│   ├── risk.txt
│   ├── ticket_to_ride.txt
│   └── uno.txt
├── specs/              # Completed component design documents
├── tests/              # Ingestion, retrieval, and generation unit tests
└── planning.md         # Recorded observations and implementation decisions
```

## Pipeline Behavior

- Rule books are split into 300-character windows with 50-character overlap.
- ChromaDB returns the three closest chunks by cosine distance.
- Chunks above distance `0.55` are excluded from the LLM context.
- The system prompt restricts answers to retrieved text and requires citations
  such as `[Catan]`.
- Empty or weak retrieval results return a fallback without calling Groq.

## Tests

```bash
python -m pytest -q
```

The automated suite does not require an API key or model download. It uses fake
ChromaDB and Groq clients to verify result mapping, filtering, prompt grounding,
citations, and fallback behavior. The real embedding pipeline was verified
against all 149 chunks, and a live Groq response was verified with a temporary
key. Running new generated answers requires `GROQ_API_KEY` in `.env`.

---

## Re-ingesting After Changes

ChromaDB persists to disk in `./chroma_db`. If you change your chunking strategy and want to re-ingest, delete that folder and restart the app:

```bash
rm -rf chroma_db/   # Mac/Linux
# or: rmdir /s chroma_db   # Windows
python app.py
```

---

## Rule Books Included

| Game | File |
|------|------|
| Catan | `docs/catan.txt` |
| Clue | `docs/clue.txt` |
| Codenames | `docs/codenames.txt` |
| Monopoly | `docs/monopoly.txt` |
| Pandemic | `docs/pandemic.txt` |
| Risk | `docs/risk.txt` |
| Ticket to Ride | `docs/ticket_to_ride.txt` |
| Uno | `docs/uno.txt` |

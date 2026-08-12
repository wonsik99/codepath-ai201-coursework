# RulesBot — System Design

**Status:** Complete
**Last updated:** March 2026

---

## Problem Statement

Board game rule books are comprehensive but inconvenient. They're structured for reference, not for answering a specific question mid-game. A player who wants to know whether they can build a settlement adjacent to an existing city has to skim through several pages to find the answer — if they can find it at all.

RulesBot solves this by making rule books queryable. A user asks a plain-language question and gets a specific answer drawn from the actual rules, with a citation so they can verify it.

The core constraint: answers must be grounded in the loaded rule books, not in what the language model already knows about the game. A confident wrong answer is worse than no answer.

---

## Architecture

RulesBot is a RAG (Retrieval-Augmented Generation) pipeline with four components:

```
User query
    │
    ▼
[1] INGEST          ──► Rule book text is chunked and stored once at startup
    ingest.py
    │
    ▼
[2] RETRIEVE        ──► Query is embedded and matched against stored chunks
    retriever.py         via semantic similarity search
    │
    ▼
[3] GENERATE        ──► Retrieved chunks are passed as context to an LLM,
    generator.py         which produces a grounded, cited answer
    │
    ▼
[4] UI              ──► Gradio chat interface serves the response to the user
    app.py
```

All four components are implemented. Retrieval converts ChromaDB's nested query
results into ranked rule chunks, and generation filters weak matches before
building a grounded, game-cited Groq request.

---

## Technical Decisions

The following decisions were made before the lab. You don't need to revisit them, but understanding the reasoning will help you implement the remaining components correctly.

### Embedding model: `all-MiniLM-L6-v2`

A lightweight sentence-transformers model that runs locally with no API key or rate limits. It maps text to 384-dimensional vectors, with good performance on short to medium passages. Tradeoffs accepted: lower accuracy than larger models (e.g., OpenAI's `text-embedding-3-large`), but no cost and no latency from network calls.

### Vector store: ChromaDB (persistent)

ChromaDB runs locally and persists its index to `./chroma_db` on disk. This means ingestion only has to happen once — subsequent startups skip it if the collection is already populated. Similarity metric is cosine distance (configured in `retriever.py`).

### LLM: Groq (`llama-3.3-70b-versatile`)

Groq provides fast inference on Llama 3.3 70B via a free API tier. The model is capable enough to follow grounding instructions reliably when they're written clearly. API key is loaded from `.env` and accessed via `config.py`.

### Distance metric: cosine similarity

Lower distance = more similar. Results from `_collection.query()` include a `distances` field — a distance of 0 means identical, and values above ~0.5 typically indicate weak relevance for this embedding model. This matters for `generate_response()`: chunks with high distances may not be relevant enough to include in context.

---

## What Is Already Built

| File | Status | What it does |
|------|--------|-------------|
| `app.py` | ✅ Complete | Gradio UI, startup orchestration, ingestion trigger |
| `config.py` | ✅ Complete | Central configuration for models, paths, retrieval params |
| `ingest.py` — `load_documents()` | ✅ Complete | Reads all `.txt` files from `/docs`, returns structured dicts |
| `ingest.py` — `chunk_document()` | ✅ Complete | Splits a document into overlapping chunks for embedding |
| `retriever.py` — ChromaDB init | ✅ Complete | Lazily initializes the client, collection, and embedding function |
| `retriever.py` — `embed_and_store()` | ✅ Complete | Embeds chunks and adds them to the collection |
| `retriever.py` — `retrieve()` | ✅ Complete | Runs semantic search and returns ranked chunks |
| `generator.py` — Groq client init | ✅ Complete | Lazily initializes a configured Groq client |
| `generator.py` — `generate_response()` | ✅ Complete | Filters context and generates a grounded, cited answer |

---

## Component Specs

The specs for the three implemented functions are in this directory:

- [`chunk-document-spec.md`](./chunk-document-spec.md)
- [`retrieve-spec.md`](./retrieve-spec.md)
- [`generate-response-spec.md`](./generate-response-spec.md)

Each spec records the final design decisions and implementation observations for
its component.

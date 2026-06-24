# AI201 Lab 4 — RepairSafe

A home repair Q&A tool with a safety classification layer. Before answering any question,
it classifies the request into one of three safety tiers (`safe`, `caution`, `refuse`) and
adjusts its behavior accordingly.

## What I Built

All three milestones are complete:

### Milestone 1 — Safety classifier (`safety.py`)
LLM-as-judge classifier with tier definitions, boundary rules (replacing vs adding), few-shot
examples, and `Tier:` / `Reason:` parsing. Falls back to `caution` on parse errors.

### Milestone 2 — Tier-aware responder (`responder.py`)
Separate system prompts per tier — full DIY steps for safe, warnings + steps for caution,
no how-to for refuse (risk explanation + licensed professional only).

### Milestone 3 — Audit logger (`auditor.py`)
Appends one JSON object per interaction to `logs/audit.jsonl` and prints a one-line
`[LOGGED]` summary to the terminal.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your GROQ_API_KEY to .env
```

## Run

```bash
python app.py
```

## Project structure

```
lab4-repairsafe/
├── app.py              # Gradio UI and pipeline orchestration (pre-built)
├── safety.py           # Milestone 1: safety tier classifier
├── responder.py        # Milestone 2: tier-aware response generator
├── auditor.py          # Milestone 3: audit logger
├── config.py           # Settings and constants
├── data/repair_tiers.md
├── logs/audit.jsonl    # written at runtime
└── specs/              # design specs (written before code)
```

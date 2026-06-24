# AI201 Lab 4 — RepairSafe

A home repair Q&A tool with a safety classification layer. Before answering any question,
it classifies the request into one of three safety tiers (`safe`, `caution`, `refuse`) and
adjusts its behavior accordingly.

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

## Lab milestones

| Milestone | Task | File |
|---|---|---|
| 1 | Classify question into safe / caution / refuse | `safety.py` |
| 2 | Generate tier-appropriate response | `responder.py` |
| 3 | Append interaction record to audit log | `auditor.py` |

Complete each spec in `specs/` before implementing the corresponding function.

## Project structure

```
lab4-repairsafe/
├── app.py              # Gradio UI and pipeline orchestration (pre-built)
├── safety.py           # Milestone 1: safety tier classifier
├── responder.py        # Milestone 2: tier-aware response generator
├── auditor.py          # Milestone 3: audit logger
├── config.py           # Settings and constants
├── requirements.txt
├── .env.example
├── data/
│   └── repair_tiers.md # Tier guide shown in the app's Tier Guide tab
├── logs/               # audit.jsonl written here after Milestone 3
└── specs/
    ├── system-design.md
    ├── classifier-spec.md
    ├── responder-spec.md
    └── auditor-spec.md
```

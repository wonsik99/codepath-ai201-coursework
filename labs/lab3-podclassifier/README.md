# AI201 Lab 3 — Pod Classifier

A few-shot podcast episode classifier. Given an episode description, classifies it
as `interview`, `solo`, `panel`, or `narrative` using labeled examples and an LLM.

## What I Built

All three milestones are complete:

### Milestone 1 — Labeled training set (`data/my_labels.json`)
Hand-labeled all 20 training episodes across the four formats
(interview 5 · solo 6 · panel 5 · narrative 4) to serve as the few-shot examples.

### Milestone 2 — Few-shot classifier (`classifier.py`)
- `load_labeled_examples()` — merges the training episodes with my labels and keeps
  only the ones with a valid, non-null label.
- `build_few_shot_prompt()` — assembles a prompt with the label definitions plus my
  labeled examples, and asks for a `Label:` / `Reasoning:` response.
- `_parse_classification_response()` — robustly extracts the label (strips quotes,
  asterisks, and punctuation, case-insensitive) and falls back to `unknown` for
  anything outside the four valid labels.
- `classify_episode()` — runs the LLM call and wraps API errors so a failure returns
  `unknown` instead of crashing the app.

### Milestone 3 — Evaluation metrics (`evaluate.py`)
- `compute_accuracy()` — overall exact-match accuracy over the held-out test set.
- `compute_per_class_accuracy()` — accuracy broken down per label (correct/total),
  which surfaces which formats the classifier struggles with.

The classifier also works with either **Groq** or **OpenAI** as the LLM backend,
selected via `LLM_PROVIDER` in the config.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Set LLM_PROVIDER to groq or openai, then add the matching API key(s)
```

## Run

```bash
python app.py
```

## Lab milestones

| Milestone | Task                              | File                  |
| --------- | --------------------------------- | --------------------- |
| 1         | Label 20 training episodes        | `data/my_labels.json` |
| 2         | Implement the few-shot classifier | `classifier.py`       |
| 3         | Implement evaluation metrics      | `evaluate.py`         |

See the lab instructions for full details.

## Project structure

```
ai201-lab3-podclassifier-starter/
├── app.py              # Gradio UI
├── classifier.py       # Few-shot classification logic
├── evaluate.py         # Evaluation metrics
├── config.py           # Settings and constants
├── requirements.txt
├── .env.example
├── data/
│   ├── train_episodes.json   # 20 episodes to label (Milestone 1)
│   ├── test_episodes.json    # 20 pre-labeled episodes (held-out test set)
│   ├── my_labels.json        # Your labels — edit this in Milestone 1
│   └── taxonomy.md           # Label definitions and edge cases
└── specs/
    ├── system-design.md      # Architecture overview
    ├── classifier-spec.md    # Spec for Milestone 2 (fill in before coding)
    └── evaluation-spec.md    # Spec for Milestone 3 (fill in before coding)
```

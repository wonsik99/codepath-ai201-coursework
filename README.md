# CodePath AI201

A collection of my weekly labs from the CodePath AI201 course.

## Labs

| Week | Lab | Description | Status |
|------|-----|-------------|--------|
| 1 | [RulesBot](./lab1-rulesbot) | Board-game rules assistant using a RAG pipeline | ⏳ Starter (to do) |
| 2 | [PlantAdvisor](./lab2-plantadvisor) | AI plant-care assistant agent built with Groq + Gradio | ✅ Done |
| 3 | [PodClassifier](./lab3-podclassifier) | Few-shot podcast episode classifier (interview/solo/panel/narrative) | ✅ Done |
| 4 | [RepairSafe](./lab4-repairsafe) | Home repair Q&A with safety tier classification (safe/caution/refuse) | ✅ Done |
| 5 | [BookClub](./lab5-bookclub) | Flask reading-list app with books, progress tracking, and stats | ⏳ Starter (to do) |

## How to run (same for every lab)

Most labs (1–4) use Gradio + an LLM API key. Lab 5 is a Flask API — see [lab5-bookclub/README.md](./lab5-bookclub/README.md) for `seed_data.py` and port 5000.

```bash
cd labN-name
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then add your own API key to .env
python app.py
```

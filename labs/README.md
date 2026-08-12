# CodePath AI201 Weekly Labs

The six weekly labs from the CodePath AI201 course, completed during Summer
2026.

| Week | Lab | Description | Status |
|---|---|---|---|
| 1 | [RulesBot](./lab1-rulesbot) | Board-game rules assistant using a RAG pipeline | Incomplete |
| 2 | [PlantAdvisor](./lab2-plantadvisor) | AI plant-care assistant agent built with Groq and Gradio | Complete |
| 3 | [PodClassifier](./lab3-podclassifier) | Few-shot podcast episode classifier | Complete |
| 4 | [RepairSafe](./lab4-repairsafe) | Home-repair Q&A with safety-tier classification | Complete |
| 5 | [BookClub](./lab5-bookclub) | Flask reading-list bug hunt | Complete |
| 6 | [GroceryList](./lab6-grocerylist) | Simulated backend pull-request review | Complete |

Lab 1 is retained as unfinished coursework. Its retrieval and generation
milestones were not completed. Labs 2-6 contain the submitted implementation or
review work.

## Running a Lab

Use the lab-specific README first. A typical Python lab starts with:

```bash
cd labs/lab2-plantadvisor
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Labs 5 and 6 are Flask APIs and require `python seed_data.py` before starting
the server.

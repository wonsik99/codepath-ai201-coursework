# CodePath AI201 Coursework

A consolidated archive of my weekly labs, standalone projects, and final
open-source contribution from the CodePath AI201 course.

**Course completed:** August 2026

## Weekly Labs

| Week | Lab | Focus | Status |
|---|---|---|---|
| 1 | [RulesBot](./labs/lab1-rulesbot) | Board-game rules assistant using a RAG pipeline | Incomplete |
| 2 | [PlantAdvisor](./labs/lab2-plantadvisor) | Tool-using plant-care agent built with Groq and Gradio | Complete |
| 3 | [PodClassifier](./labs/lab3-podclassifier) | Few-shot podcast episode classifier with evaluation metrics | Complete |
| 4 | [RepairSafe](./labs/lab4-repairsafe) | Safety-tiered home-repair assistant with audit logging | Complete |
| 5 | [BookClub](./labs/lab5-bookclub) | Flask bug hunt covering reading streaks and history ordering | Complete |
| 6 | [GroceryList](./labs/lab6-grocerylist) | Code review of two simulated backend pull requests | Complete |

Lab 1 remains an intentionally honest record of unfinished coursework: document
chunking is present, but retrieval and response generation are still stubs.

## Standalone Projects

| Project | Name | Description |
|---|---|---|
| 1 | [The Unofficial Guide](./projects/project1) | RAG system for choosing UMich CS/EECS courses with source-attributed answers |
| 2 | [FitFindr](./projects/project2) | Outfit-recommendation agent over secondhand listings and a user wardrobe |
| 3 | [TakeMeter](./projects/project3) | Fine-tuned classifier for `r/soccer` discourse quality and comment type |
| 4 | [Provenance Guard](./projects/project4) | Attribution backend for distinguishing human-written and AI-generated creative text |
| 5 | [Mixtape Bug Hunt](./projects/project5) | Flask social-music app bug hunt with root-cause documentation |
| 6 | [CineLog](./projects/project6) | Simulated code review, UUID rebase, and commit-history rewrite exercise |

## Open-Source Contribution: PathReview

Weeks 7-10 focused on contributing to
[PathReview](https://github.com/ascherj/pathreview), an existing AI-powered
portfolio review application. My contribution added 14 integration tests for
the safety pipeline (`PromptDefense -> ContentFilter -> BiasDetector ->
PIIScrubber`).

- [Contribution archive](./contributions/pathreview)
- [Issue #75](https://github.com/ascherj/pathreview/issues/75)
- [Upstream PR #323](https://github.com/ascherj/pathreview/pull/323)
- [Contribution fork](https://github.com/wonsik99/pathreview)

The coursework and Week 10 reflection are complete. The upstream pull request
was still open when this archive was consolidated on August 12, 2026.

## Running the Work

Each lab and project has its own README and dependency list. Start from the
specific directory rather than the repository root:

```bash
cd labs/lab2-plantadvisor  # or projects/project1
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # when the project provides one
python app.py
```

Some projects use a different entry point or require seed data; follow their
local README for the authoritative instructions.

## Git History

This repository preserves both original coursework histories without
squashing. The pre-consolidation endpoints are also marked by these tags:

- `archive/ai201-projects-final`
- `archive/codepath-ai201-final`

PathReview remains a separate fork while its upstream pull request is open; its
source code is linked rather than vendored here.

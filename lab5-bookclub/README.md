# AI201 Lab 5 — BookClub

A small reading list app where club members track books, log their progress, and see their reading stats.

## What the app does

- **Book list** — members add books to a shared reading list
- **Reading tracker** — mark books as started or finished
- **Stats** — reading streak, books finished this month, total pages read

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # optional — defaults work for local dev
python seed_data.py    # populate the database
```

## Run

```bash
python app.py          # http://127.0.0.1:5000
```

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/books/` | List all books |
| POST | `/books/` | Add a book |
| POST | `/reading/start` | Mark a book as started |
| POST | `/reading/finish` | Mark a book as finished |
| GET | `/reading/current/<user_id>` | Books a user is currently reading |
| GET | `/reading/history/<user_id>` | Books a user has finished |
| GET | `/stats/<user_id>` | Reading streak, books this month, total pages |

## Project structure

```
lab5-bookclub/
├── app.py                  Flask application factory
├── models.py               SQLAlchemy models: User, Book, ReadingEvent
├── seed_data.py            Database seed script
├── routes/
│   ├── books.py            Book list endpoints
│   ├── reading.py          Reading progress endpoints
│   └── stats.py            Statistics endpoint
└── services/
    ├── reading_service.py  Reading list business logic
    └── stats_service.py    Statistics calculations
```

## Example requests

After seeding, `seed_data.py` prints user IDs. Then:

```bash
curl http://127.0.0.1:5000/books/
curl http://127.0.0.1:5000/stats/USER_ID
curl http://127.0.0.1:5000/reading/history/USER_ID
```

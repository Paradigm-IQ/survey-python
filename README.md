# Employee Survey

A small employee survey tool: **create a survey, collect responses, view results.**

Stack: Python 3.12 · [uv](https://docs.astral.sh/uv/) · FastAPI · SQLModel · SQLite · Jinja2 templates · plain HTML/CSS (no build step).

## Run

```sh
uv run uvicorn app.main:app --reload
```

Then open http://127.0.0.1:8000. (`uv run` installs dependencies on first use.)

Tests: `uv run pytest`

## Layout

```
app/
  main.py        FastAPI app, startup (creates tables), static mount
  db.py          engine + session dependency (SQLite file: ./survey.db)
  models.py      SQLModel tables  <- only Survey exists; questions/responses/answers are TODO
  routes.py      HTML routes      <- survey list/create done; the rest are TODO
  seed.py        sample data (`uv run python -m app.seed`)
  templates/     Jinja2 pages (base, index, new, take, results)
  static/        style.css
tests/           pytest + TestClient against an in-memory SQLite DB
```

## Status

| Flow                          | Route                                  | State |
|-------------------------------|----------------------------------------|-------|
| List surveys                  | `GET /`                                | ✅    |
| Create survey (title, description) | `GET /surveys/new`, `POST /surveys` | ✅    |
| Question builder (on the new-survey form) | `POST /surveys`            | TODO  |
| Take survey                   | `GET /surveys/{id}`                    | TODO (placeholder) |
| Submit response               | `POST /surveys/{id}/responses`         | TODO (501) |
| View results                  | `GET /surveys/{id}/results`            | TODO (placeholder) |

Everything involving questions, responses, and results is stubbed. Search for `TODO`.

## Notes

- No migrations: tables are created on startup. After changing a model, `rm survey.db` and restart.
- Sample data: `uv run python -m app.seed` (reset: `rm survey.db && uv run python -m app.seed`).
- `SQL_ECHO=1` logs SQL; `DATABASE_URL` overrides the DB location.

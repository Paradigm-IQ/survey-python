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
  models.py      SQLModel tables  <- Survey done; Question/Response/Answer are TODO
  routes.py      HTML routes      <- survey list/create done; the rest are TODO
  templates/     Jinja2 pages (base, index, new, edit, take, results)
  static/        style.css
tests/           pytest + TestClient against an in-memory SQLite DB
```

## Status

| Flow                          | Route                                  | State |
|-------------------------------|----------------------------------------|-------|
| List surveys                  | `GET /`                                | ✅    |
| Create survey                 | `GET /surveys/new`, `POST /surveys`    | ✅    |
| Add questions                 | `POST /surveys/{id}/questions`         | TODO (501) |
| Take survey / submit response | `GET /surveys/{id}/take`, `POST /surveys/{id}/responses` | TODO (501) |
| View results                  | `GET /surveys/{id}/results`            | TODO (placeholder) |

## Notes

- No migrations: tables are created on startup. After changing a model, `rm survey.db` and restart.
- `SQL_ECHO=1` logs SQL; `DATABASE_URL` overrides the DB location.

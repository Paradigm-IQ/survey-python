"""Data model for the employee survey tool.

Only Survey exists; questions/responses/answers are TODO.

No migrations: tables are created on startup. After changing a model,
`rm survey.db` and restart.
"""

from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


def utcnow() -> datetime:
    return datetime.now(UTC)


class Survey(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str = ""
    created_at: datetime = Field(default_factory=utcnow)


# TODO: questions
#   - which survey it belongs to, prompt text, ordering
#   - question type? (e.g. rating 1-5, free text, multiple choice)
#   - multiple choice options -- column (JSON) or separate table?

# TODO: responses
#   - one submission of a survey by one employee
#   - anonymous vs. identified? submitted timestamp?

# TODO: answers
#   - one row per (response, question) with the value

"""Data layer.

Survey is wired end-to-end as an example of the pattern.
Everything else is a TODO -- decide the shape together.

Open questions worth discussing before writing code:
  - Question types: free text? 1-5 rating (Likert)? multiple choice? Which first?
  - Is a survey editable after it has responses? Draft / published / closed states?
  - Anonymous responses vs. tied to an employee? (Trust matters for employee surveys.)
  - How should results be aggregated per question type?
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

    # TODO: relationship to questions, e.g.
    #   questions: list["Question"] = Relationship(back_populates="survey")
    # TODO: status (draft/open/closed)?


# TODO: Question
#   - belongs to a Survey (survey_id FK)
#   - prompt text, kind (text / rating / choice), position/order, required?
#   - choice options: separate table, or JSON column?
#
# class Question(SQLModel, table=True):
#     ...


# TODO: Response -- one employee's submission of one survey
#   - survey_id FK, submitted_at
#   - respondent identity (or deliberately none, for anonymity)
#
# class Response(SQLModel, table=True):
#     ...


# TODO: Answer -- one answer to one question within a Response
#   - response_id FK, question_id FK
#   - value storage: single text column? separate int column for ratings?
#
# class Answer(SQLModel, table=True):
#     ...

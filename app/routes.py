"""HTML routes (server-rendered with Jinja2, plain <form> posts, no JS build).

Flow:  list surveys -> create survey -> add questions -> take survey -> view results
"""

from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from app.db import get_session
from app.models import Survey

templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
router = APIRouter()

SessionDep = Annotated[Session, Depends(get_session)]


def get_survey_or_404(session: Session, survey_id: int) -> Survey:
    survey = session.get(Survey, survey_id)
    if survey is None:
        raise HTTPException(status_code=404, detail="Survey not found")
    return survey


# --- Surveys (working example) -------------------------------------------------


@router.get("/", response_class=HTMLResponse)
def list_surveys(request: Request, session: SessionDep):
    surveys = session.exec(select(Survey).order_by(Survey.created_at.desc())).all()
    return templates.TemplateResponse(request, "index.html", {"surveys": surveys})


@router.get("/surveys/new", response_class=HTMLResponse)
def new_survey_form(request: Request):
    return templates.TemplateResponse(request, "survey_new.html", {})


@router.post("/surveys")
def create_survey(
    session: SessionDep,
    title: Annotated[str, Form()],
    description: Annotated[str, Form()] = "",
):
    # TODO: validation (blank title, length limits) and re-render form with errors.
    survey = Survey(title=title.strip(), description=description.strip())
    session.add(survey)
    session.commit()
    session.refresh(survey)
    return RedirectResponse(f"/surveys/{survey.id}/edit", status_code=303)


# --- Questions -----------------------------------------------------------------


@router.get("/surveys/{survey_id}/edit", response_class=HTMLResponse)
def edit_survey(request: Request, survey_id: int, session: SessionDep):
    survey = get_survey_or_404(session, survey_id)
    # TODO: load the survey's questions once the Question model exists.
    questions: list = []
    return templates.TemplateResponse(
        request, "survey_edit.html", {"survey": survey, "questions": questions}
    )


@router.post("/surveys/{survey_id}/questions")
def add_question(
    survey_id: int,
    session: SessionDep,
    prompt: Annotated[str, Form()],
    kind: Annotated[str, Form()] = "text",
):
    get_survey_or_404(session, survey_id)
    # TODO: create a Question(survey_id=..., prompt=..., kind=..., position=...)
    raise HTTPException(status_code=501, detail="TODO: add_question")


# --- Responses -----------------------------------------------------------------


@router.get("/surveys/{survey_id}/take", response_class=HTMLResponse)
def take_survey(request: Request, survey_id: int, session: SessionDep):
    survey = get_survey_or_404(session, survey_id)
    # TODO: load questions and render an input per question kind.
    questions: list = []
    return templates.TemplateResponse(
        request, "survey_take.html", {"survey": survey, "questions": questions}
    )


@router.post("/surveys/{survey_id}/responses")
async def submit_response(request: Request, survey_id: int, session: SessionDep):
    get_survey_or_404(session, survey_id)
    form = await request.form()  # fields named like "q_<question_id>"
    # TODO: create a Response + one Answer per question; validate required/ratings.
    raise HTTPException(status_code=501, detail=f"TODO: submit_response ({len(form)} fields)")


# --- Results -------------------------------------------------------------------


@router.get("/surveys/{survey_id}/results", response_class=HTMLResponse)
def survey_results(request: Request, survey_id: int, session: SessionDep):
    survey = get_survey_or_404(session, survey_id)
    # TODO: aggregate answers per question:
    #   rating -> count, average, distribution
    #   choice -> count per option
    #   text   -> list of answers
    response_count = 0
    results: list = []
    return templates.TemplateResponse(
        request,
        "survey_results.html",
        {"survey": survey, "response_count": response_count, "results": results},
    )

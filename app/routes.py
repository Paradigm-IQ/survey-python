"""HTML routes (server-rendered with Jinja2, plain <form> posts, no JS build).

Flow:  list surveys -> create survey (with questions) -> take survey -> view results
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
    # TODO: also load the survey's questions
    survey = session.get(Survey, survey_id)
    if survey is None:
        raise HTTPException(status_code=404, detail="Survey not found")
    return survey


# --- Surveys -------------------------------------------------------------------


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
    title = title.strip()

    # TODO: validation + error handling (re-render the form with errors?)
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")

    # TODO: collect questions from the form and insert them alongside the
    # survey (same transaction?)
    survey = Survey(title=title, description=description.strip())
    session.add(survey)
    session.commit()
    session.refresh(survey)
    return RedirectResponse(f"/surveys/{survey.id}", status_code=303)


# --- Responses -----------------------------------------------------------------


@router.get("/surveys/{survey_id}", response_class=HTMLResponse)
def take_survey(request: Request, survey_id: int, session: SessionDep):
    survey = get_survey_or_404(session, survey_id)
    return templates.TemplateResponse(request, "survey_take.html", {"survey": survey})


@router.post("/surveys/{survey_id}/responses")
async def submit_response(request: Request, survey_id: int, session: SessionDep):
    get_survey_or_404(session, survey_id)
    form = await request.form()
    # TODO: validate answers against the survey's questions
    # TODO: persist a response + its answers, then redirect to results
    raise HTTPException(status_code=501, detail=f"TODO: submit_response ({len(form)} fields)")


# --- Results -------------------------------------------------------------------


@router.get("/surveys/{survey_id}/results", response_class=HTMLResponse)
def survey_results(request: Request, survey_id: int, session: SessionDep):
    survey = get_survey_or_404(session, survey_id)
    # TODO: aggregate answers per question (counts, averages, free-text list...)
    return templates.TemplateResponse(request, "survey_results.html", {"survey": survey})

from sqlmodel import select

from app.models import Survey


def test_healthz(client):
    assert client.get("/healthz").json() == {"status": "ok"}


def test_index_empty(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "No surveys yet" in resp.text


def test_create_survey(client, session):
    resp = client.post(
        "/surveys",
        data={"title": "Q4 Engagement", "description": "Quarterly pulse"},
        follow_redirects=False,
    )
    assert resp.status_code == 303

    survey = session.exec(select(Survey)).one()
    assert survey.title == "Q4 Engagement"
    assert resp.headers["location"] == f"/surveys/{survey.id}/edit"
    assert "Q4 Engagement" in client.get("/").text


def test_missing_survey_404(client):
    assert client.get("/surveys/999/results").status_code == 404


# TODO: test_add_question
# TODO: test_submit_response
# TODO: test_results_aggregation (e.g. rating average across responses)

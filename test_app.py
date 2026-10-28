
import pytest
from app import app, QUESTIONS


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Online Exam System" in response.data


def test_all_questions_displayed(client):
    response = client.get("/")
    assert response.status_code == 200

    for question in QUESTIONS:
        assert question["question"].encode() in response.data


def test_question_count():
    assert len(QUESTIONS) == 5


def test_valid_submission(client):
    answers = {
        str(q["id"]): q["correct_answer"]
        for q in QUESTIONS
    }

    response = client.post("/submit", json={"answers": answers})

    assert response.status_code == 200
    assert response.json["submitted"] is True
    assert response.json["score"] == 5
    assert response.json["total"] == 5


def test_one_wrong_answer_scores_four(client):
    answers = {
        str(q["id"]): q["correct_answer"]
        for q in QUESTIONS
    }
    answers["1"] = "Python"

    response = client.post("/submit", json={"answers": answers})

    assert response.status_code == 200
    assert response.json["score"] == 4
    assert response.json["total"] == 5


def test_empty_answers_score_zero(client):
    response = client.post("/submit", json={"answers": {}})

    assert response.status_code == 200
    assert response.json["score"] == 0
    assert response.json["total"] == 5


def test_invalid_submission(client):
    response = client.post("/submit", json={"answers": []})
    assert response.status_code == 400


def test_invalid_question_id(client):
    response = client.post(
        "/submit",
        json={"answers": {"999": "HTML"}}
    )
    assert response.status_code == 400


def test_invalid_answer_option(client):
    response = client.post(
        "/submit",
        json={"answers": {"1": "Invalid Option"}}
    )
    assert response.status_code == 400

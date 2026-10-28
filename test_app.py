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
        str(q["id"]): q["options"][0]
        for q in QUESTIONS
    }
    response = client.post("/submit", json={"answers": answers})
    assert response.status_code == 200
    assert response.json["submitted"] is True
def test_invalid_submission(client):
    response = client.post("/submit", json={"answers": []})
    assert response.status_code == 400
def test_invalid_answer_option(client):
    response = client.post(
        "/submit",
        json={"answers": {"1": "Invalid Option"}}
    )
    assert response.status_code == 400

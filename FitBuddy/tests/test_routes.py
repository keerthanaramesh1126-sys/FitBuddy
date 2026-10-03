import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch
from app.main import app
from app.models import Base
from app import database as db_module


@pytest.fixture(autouse=True)
def setup_test_db(tmp_path, monkeypatch):
    db_file = str(tmp_path / "test.db")
    engine = create_engine(f"sqlite:///{db_file}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine)
    monkeypatch.setattr(db_module, "SessionLocal", TestSession)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def client():
    with TestClient(app, raise_server_exceptions=True) as c:
        yield c


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "FitBuddy" in response.text


def test_login_page(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert "Admin Login" in response.text


def test_login_invalid(client):
    response = client.post("/login", data={"username": "wrong", "password": "wrong"})
    assert response.status_code == 200
    assert "Invalid" in response.text


def test_admin_redirect_unauthenticated(client):
    response = client.get("/admin", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers.get("location", "")


def test_logout(client):
    response = client.get("/logout", follow_redirects=False)
    assert response.status_code == 302


@patch("app.routes.generate_workout_gemini", return_value="Day 1: Squats 3x15")
@patch("app.routes.generate_nutrition_tip_with_flash", return_value="Stay hydrated")
def test_generate_workout_valid(mock_tip, mock_workout, client):
    response = client.post("/generate-workout", data={
        "username": "TestUser",
        "user_id": "100",
        "age": "25",
        "weight": "70",
        "goal": "weight loss",
        "intensity": "medium",
    })
    assert response.status_code == 200
    assert "Day 1" in response.text


def test_generate_workout_invalid_age(client):
    response = client.post("/generate-workout", data={
        "username": "TestUser",
        "user_id": "101",
        "age": "5",
        "weight": "70",
        "goal": "weight loss",
        "intensity": "medium",
    })
    assert response.status_code == 200
    assert "Age must be" in response.text


def test_generate_workout_missing_username(client):
    response = client.post("/generate-workout", data={
        "username": "   ",
        "user_id": "102",
        "age": "25",
        "weight": "70",
        "goal": "weight loss",
        "intensity": "medium",
    })
    assert response.status_code == 200
    assert "required" in response.text.lower()


def test_submit_feedback_no_plan(client):
    response = client.post("/submit-feedback", data={
        "user_id": "999",
        "feedback": "I want more cardio please",
    })
    assert response.status_code == 200
    assert "No workout plan" in response.text


@patch("app.routes.generate_workout_gemini", return_value="Day 1: Running 30 min")
@patch("app.routes.generate_nutrition_tip_with_flash", return_value="Eat vegetables")
@patch("app.routes.update_workout_plan", return_value="Day 1: Home Running 30 min")
def test_submit_feedback_with_plan(mock_update, mock_tip, mock_workout, client):
    client.post("/generate-workout", data={
        "username": "FeedbackUser",
        "user_id": "200",
        "age": "28",
        "weight": "65",
        "goal": "general wellness",
        "intensity": "low",
    })
    response = client.post("/submit-feedback", data={
        "user_id": "200",
        "feedback": "I prefer outdoor workouts",
    })
    assert response.status_code == 200
    assert "updated" in response.text.lower()


def test_view_all_users_redirect(client):
    response = client.get("/view-all-users", follow_redirects=False)
    assert response.status_code == 302

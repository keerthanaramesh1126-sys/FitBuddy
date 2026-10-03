git import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, User, WorkoutPlan, Feedback
from app import database as db_module


@pytest.fixture(autouse=True)
def test_db(tmp_path, monkeypatch):
    db_file = str(tmp_path / "test.db")
    engine = create_engine(f"sqlite:///{db_file}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine)
    monkeypatch.setattr(db_module, "SessionLocal", TestSession)
    yield
    Base.metadata.drop_all(engine)


def test_save_and_get_user():
    db_module.save_user(1, "Alice", 25, 60.0, "weight loss", "medium")
    user = db_module.get_user(1)
    assert user is not None
    assert user.username == "Alice"
    assert user.age == 25


def test_save_duplicate_user():
    db_module.save_user(1, "Alice", 25, 60.0, "weight loss", "medium")
    db_module.save_user(1, "Alice Updated", 26, 61.0, "muscle gain", "high")
    user = db_module.get_user(1)
    assert user.username == "Alice Updated"


def test_get_nonexistent_user():
    result = db_module.get_user(9999)
    assert result is None


def test_save_and_get_plan():
    db_module.save_user(2, "Bob", 30, 80.0, "muscle gain", "high")
    db_module.save_plan(2, "Day 1: Push-ups", "Eat protein")
    original = db_module.get_original_plan(2)
    assert original == "Day 1: Push-ups"


def test_update_plan():
    db_module.save_user(3, "Carol", 28, 55.0, "flexibility", "low")
    db_module.save_plan(3, "Day 1: Yoga", "Stay hydrated")
    db_module.update_plan(3, "Day 1: Advanced Yoga")
    session = db_module.SessionLocal()
    plan = session.query(WorkoutPlan).filter(WorkoutPlan.user_id == 3).first()
    session.close()
    assert plan.updated_plan == "Day 1: Advanced Yoga"
    assert plan.original_plan == "Day 1: Yoga"


def test_get_original_plan_no_plan():
    result = db_module.get_original_plan(8888)
    assert result is None


def test_get_all_users():
    db_module.save_user(10, "User10", 20, 50.0, "weight loss", "low")
    db_module.save_user(11, "User11", 21, 55.0, "muscle gain", "medium")
    users = db_module.get_all_users()
    assert len(users) >= 2


def test_save_feedback():
    db_module.save_user(4, "Dave", 35, 90.0, "general wellness", "medium")
    db_module.save_feedback(4, "I prefer home workouts")
    session = db_module.SessionLocal()
    fb = session.query(Feedback).filter(Feedback.user_id == 4).first()
    session.close()
    assert fb is not None
    assert "home" in fb.feedback_text

import pytest
from unittest.mock import patch, MagicMock


def make_mock_response(text):
    mock = MagicMock()
    mock.text = text
    return mock


@patch("app.gemini_generator.genai.GenerativeModel")
def test_generate_workout_success(mock_model_cls):
    mock_model = MagicMock()
    mock_model.generate_content.return_value = make_mock_response("Day 1: Push-ups 3x10")
    mock_model_cls.return_value = mock_model

    from app.gemini_generator import generate_workout_gemini
    result = generate_workout_gemini({"goal": "weight loss", "intensity": "medium", "age": 25, "weight": 70})
    assert "Day 1" in result


@patch("app.gemini_generator.genai.GenerativeModel")
def test_generate_workout_failure(mock_model_cls):
    mock_model = MagicMock()
    mock_model.generate_content.side_effect = Exception("API error")
    mock_model_cls.return_value = mock_model

    from app.gemini_generator import generate_workout_gemini
    result = generate_workout_gemini({"goal": "muscle gain", "intensity": "high", "age": 30, "weight": 80})
    assert "Error" in result


@patch("app.gemini_flash_generator.genai.GenerativeModel")
def test_generate_nutrition_tip_success(mock_model_cls):
    mock_model = MagicMock()
    mock_model.generate_content.return_value = make_mock_response("Eat lean protein after workouts.")
    mock_model_cls.return_value = mock_model

    from app.gemini_flash_generator import generate_nutrition_tip_with_flash
    result = generate_nutrition_tip_with_flash("muscle gain")
    assert len(result) > 0


@patch("app.gemini_flash_generator.genai.GenerativeModel")
def test_generate_nutrition_tip_failure(mock_model_cls):
    mock_model = MagicMock()
    mock_model.generate_content.side_effect = Exception("API error")
    mock_model_cls.return_value = mock_model

    from app.gemini_flash_generator import generate_nutrition_tip_with_flash
    result = generate_nutrition_tip_with_flash("flexibility")
    assert "Error" in result


@patch("app.updated_plan.genai.GenerativeModel")
def test_update_workout_plan_success(mock_model_cls):
    mock_model = MagicMock()
    mock_model.generate_content.return_value = make_mock_response("Day 1: Home workouts only")
    mock_model_cls.return_value = mock_model

    from app.updated_plan import update_workout_plan
    result = update_workout_plan("Day 1: Gym workouts", "I prefer home workouts")
    assert "Day 1" in result


@patch("app.updated_plan.genai.GenerativeModel")
def test_update_workout_plan_failure(mock_model_cls):
    mock_model = MagicMock()
    mock_model.generate_content.side_effect = Exception("API error")
    mock_model_cls.return_value = mock_model

    from app.updated_plan import update_workout_plan
    result = update_workout_plan("original plan", "feedback")
    assert "Error" in result

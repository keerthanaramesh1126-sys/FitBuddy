import google.generativeai as genai
from .config import settings

genai.configure(api_key=settings.google_api_key)


def generate_workout_gemini(user_input: dict) -> str:
    age = user_input["age"]
    weight = user_input["weight"]
    goal = user_input["goal"]
    intensity = user_input["intensity"]
    prompt = (
        "You are a certified personal trainer. "
        "Create a detailed 7-day workout plan for: "
        "Age=" + str(age) + " years, Weight=" + str(weight) + " kg, "
        "Goal=" + goal + ", Intensity=" + intensity + ". "
        "Format each day as: Day N: Name - Focus / exercise list with sets/reps. "
        "Include 7 days with one rest day. Keep exercises safe."
    )
    try:
        model = genai.GenerativeModel(settings.gemini_workout_model)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "Error generating workout plan: " + str(e)

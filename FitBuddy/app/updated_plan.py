import google.generativeai as genai
from .config import settings

genai.configure(api_key=settings.google_api_key)


def update_workout_plan(original_plan: str, user_feedback: str) -> str:
    prompt = (
        "You are a certified personal fitness trainer. "
        "Here is a user's current 7-day workout plan: "
        + original_plan
        + " User feedback: "
        + user_feedback
        + " Based on this feedback, revise only the relevant parts of the plan. "
        "Keep the same 7-day format. Preserve unchanged days. "
        "Do not add extreme or unsafe exercises. Return the complete updated 7-day plan."
    )
    try:
        model = genai.GenerativeModel(settings.gemini_workout_model)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "Error updating plan: " + str(e)

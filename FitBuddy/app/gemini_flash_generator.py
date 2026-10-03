import google.generativeai as genai
from .config import settings

genai.configure(api_key=settings.google_api_key)


def generate_nutrition_tip_with_flash(goal: str) -> str:
    """Generate a concise nutrition/recovery tip using Gemini."""
    prompt = (
        f"Give one clear, practical nutrition or recovery tip for someone focused on '{goal}'. "
        "The tip should be specific, actionable, and easy to understand. "
        "Keep it to 2-3 sentences. Avoid extreme dietary advice. "
        "Focus on balanced, sustainable habits."
    )
    try:
        model = genai.GenerativeModel(settings.gemini_tip_model)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating nutrition tip: {str(e)}"

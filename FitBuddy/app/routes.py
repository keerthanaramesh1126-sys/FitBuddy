import os
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from . import database as db
from .gemini_generator import generate_workout_gemini
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .updated_plan import update_workout_plan
from .auth import check_admin, create_session_token, verify_session_token, SESSION_COOKIE

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
router = APIRouter()


def _tr(request, name, context=None):
    return templates.TemplateResponse(request, name, context or {})


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return _tr(request, "index.html")


@router.post("/generate-workout", response_class=HTMLResponse)
async def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: int = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
):
    errors = []
    if not username.strip():
        errors.append("Username is required.")
    if age < 10 or age > 100:
        errors.append("Age must be between 10 and 100.")
    if weight <= 0 or weight > 500:
        errors.append("Weight must be a positive number.")
    if goal not in ["weight loss", "muscle gain", "general wellness", "flexibility"]:
        errors.append("Invalid fitness goal selected.")
    if intensity not in ["low", "medium", "high"]:
        errors.append("Invalid workout intensity selected.")
    if errors:
        return _tr(request, "index.html", {
            "errors": errors,
            "form_data": {
                "username": username, "user_id": user_id,
                "age": age, "weight": weight, "goal": goal, "intensity": intensity
            }
        })
    db.save_user(user_id, username.strip(), age, weight, goal, intensity)
    plan = generate_workout_gemini({"goal": goal, "intensity": intensity, "age": age, "weight": weight})
    nutrition_tip = generate_nutrition_tip_with_flash(goal)
    db.save_plan(user_id, plan, nutrition_tip)
    return _tr(request, "result.html", {
        "username": username.strip(), "user_id": user_id, "age": age,
        "weight": weight, "goal": goal, "intensity": intensity,
        "workout_plan": plan, "nutrition_tip": nutrition_tip,
        "updated_plan": None, "success_message": None
    })


@router.post("/submit-feedback", response_class=HTMLResponse)
async def submit_feedback(
    request: Request,
    user_id: int = Form(...),
    feedback: str = Form(...),
):
    if not feedback.strip() or len(feedback.strip()) < 5:
        return _tr(request, "result.html", {
            "error_message": "Feedback must be at least 5 characters.",
            "user_id": user_id
        })
    original = db.get_original_plan(user_id)
    if not original:
        return _tr(request, "result.html", {
            "error_message": "No workout plan found for this User ID. Generate a plan first.",
            "user_id": user_id
        })
    db.save_feedback(user_id, feedback.strip())
    revised = update_workout_plan(original, feedback.strip())
    db.update_plan(user_id, revised)
    user = db.get_user(user_id)
    from .models import WorkoutPlan
    from .database import SessionLocal
    session = SessionLocal()
    try:
        plan_row = session.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
    finally:
        session.close()
    return _tr(request, "result.html", {
        "username": user.username if user else "",
        "user_id": user_id,
        "age": user.age if user else "",
        "weight": user.weight if user else "",
        "goal": user.goal if user else "",
        "intensity": user.intensity if user else "",
        "workout_plan": original,
        "nutrition_tip": plan_row.nutrition_tip if plan_row else "",
        "updated_plan": revised,
        "success_message": "Your plan has been updated based on your feedback!"
    })


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    token = request.cookies.get(SESSION_COOKIE)
    if token and verify_session_token(token):
        return RedirectResponse("/admin", status_code=302)
    return _tr(request, "login.html")


@router.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    if check_admin(username, password):
        token = create_session_token(username)
        response = RedirectResponse("/admin", status_code=302)
        response.set_cookie(SESSION_COOKIE, token, httponly=True, samesite="lax", max_age=3600)
        return response
    return _tr(request, "login.html", {"error": "Invalid username or password."})


@router.get("/logout")
async def logout():
    response = RedirectResponse("/login", status_code=302)
    response.delete_cookie(SESSION_COOKIE)
    return response


@router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    token = request.cookies.get(SESSION_COOKIE)
    if not token or not verify_session_token(token):
        return RedirectResponse("/login", status_code=302)
    users = db.get_all_users()
    plans = db.get_all_plans()
    plan_map = {p.user_id: p for p in plans}
    user_data = [
        {
            "id": u.user_id,
            "name": u.username,
            "age": u.age,
            "weight": u.weight,
            "goal": u.goal,
            "intensity": u.intensity,
            "original_plan": plan_map[u.user_id].original_plan if u.user_id in plan_map else "N/A",
            "updated_plan": (plan_map[u.user_id].updated_plan
                             if u.user_id in plan_map and plan_map[u.user_id].updated_plan
                             else "Not updated"),
            "nutrition_tip": plan_map[u.user_id].nutrition_tip if u.user_id in plan_map else "",
        }
        for u in users
    ]
    stats = {
        "total_users": len(users),
        "total_plans": len(plans),
        "total_updated": sum(1 for p in plans if p.updated_plan),
    }
    return _tr(request, "all_users.html", {"users": user_data, "stats": stats})


@router.get("/view-all-users", response_class=HTMLResponse)
async def view_all_users_redirect():
    return RedirectResponse("/admin", status_code=302)

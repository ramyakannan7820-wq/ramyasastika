import os

from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

import database as db
from gemini_flash_generator import generate_nutrition_tip_with_flash
from gemini_generator import generate_workout_gemini
from schemas import FeedbackRequest, UserInput
from updated_plan import update_workout_plan

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
router = APIRouter()


def _result(request, user, plan, message=None):
    return templates.TemplateResponse(request, "result.html", {
        "username": user.username, "user_id": user.user_id,
        "age": user.age, "weight": user.weight, "goal": user.goal,
        "intensity": user.intensity, "workout_plan": plan,
        "nutrition_tip": user.nutrition_tip, "message": message,
    })


def _error(request, msg):
    return templates.TemplateResponse(request, "index.html", {"error": msg}, status_code=400)


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"error": None})


@router.post("/generate-workout")
def generate_workout(request: Request, username: str = Form(...), user_id: str = Form(...),
                     age: int = Form(...), weight: float = Form(...),
                     goal: str = Form(...), intensity: str = Form(...)):
    try:
        data = UserInput(username=username.strip(), user_id=user_id.strip(), age=age,
                         weight=weight, goal=goal, intensity=intensity)
    except ValidationError:
        return _error(request, "Please check your details (age 10-100, weight 1-400 kg).")
    db.save_user(data)
    plan = generate_workout_gemini(data.age, data.weight, data.goal, data.intensity)
    tip = generate_nutrition_tip_with_flash(data.goal)
    db.save_plan(data.user_id, plan, tip)
    return _result(request, db.get_user(data.user_id), plan)


@router.post("/submit-feedback")
def submit_feedback(request: Request, user_id: str = Form(...), feedback: str = Form(...)):
    try:
        fb = FeedbackRequest(user_id=user_id.strip(), feedback=feedback.strip())
    except ValidationError:
        return _error(request, "Feedback cannot be empty.")
    user = db.get_user(fb.user_id)
    if not user or not user.original_plan:
        return _error(request, f"No plan found for User ID '{fb.user_id}'. Generate one first.")
    base = user.updated_plan or user.original_plan
    new_plan = update_workout_plan(base, fb.feedback)
    db.update_plan(fb.user_id, new_plan)
    return _result(request, user, new_plan, "Your plan has been updated based on your feedback!")


@router.get("/view-all-users")
def view_all_users(request: Request):
    return templates.TemplateResponse(request, "all_users.html", {"users": db.get_all_users()})


@router.post("/delete-user")
def delete_user(user_id: str = Form(...)):
    db.delete_user(user_id)
    return RedirectResponse("/view-all-users", status_code=303)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    from . import models  # noqa: F401
    Base.metadata.create_all(bind=engine)


def save_user(user_id, username, age, weight, goal, intensity):
    from .models import User
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.user_id == user_id).first()
        if user:
            user.username  = username
            user.age       = age
            user.weight    = weight
            user.goal      = goal
            user.intensity = intensity
        else:
            session.add(User(user_id=user_id, username=username, age=age,
                             weight=weight, goal=goal, intensity=intensity))
        session.commit()
    finally:
        session.close()


def get_user(user_id):
    from .models import User
    session = SessionLocal()
    try:
        return session.query(User).filter(User.user_id == user_id).first()
    finally:
        session.close()


def get_all_users():
    from .models import User
    session = SessionLocal()
    try:
        return session.query(User).all()
    finally:
        session.close()


def save_plan(user_id, original_plan, nutrition_tip=None):
    from .models import WorkoutPlan
    session = SessionLocal()
    try:
        plan = session.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
        if plan:
            plan.original_plan = original_plan
            plan.nutrition_tip = nutrition_tip
            plan.updated_plan  = None
        else:
            session.add(WorkoutPlan(user_id=user_id, original_plan=original_plan,
                                    nutrition_tip=nutrition_tip))
        session.commit()
    finally:
        session.close()


def update_plan(user_id, updated_plan):
    from .models import WorkoutPlan
    session = SessionLocal()
    try:
        plan = session.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
        if plan:
            plan.updated_plan = updated_plan
            session.commit()
    finally:
        session.close()


def get_original_plan(user_id):
    from .models import WorkoutPlan
    session = SessionLocal()
    try:
        plan = session.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
        return plan.original_plan if plan else None
    finally:
        session.close()


def get_all_plans():
    from .models import WorkoutPlan
    session = SessionLocal()
    try:
        return session.query(WorkoutPlan).all()
    finally:
        session.close()


def save_feedback(user_id, feedback_text):
    from .models import Feedback
    session = SessionLocal()
    try:
        session.add(Feedback(user_id=user_id, feedback_text=feedback_text))
        session.commit()
    finally:
        session.close()

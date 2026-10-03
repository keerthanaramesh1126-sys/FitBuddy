from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    user_id   = Column(Integer, primary_key=True, index=True)
    username  = Column(String(100), nullable=False)
    age       = Column(Integer, nullable=False)
    weight    = Column(Float, nullable=False)
    goal      = Column(String(50), nullable=False)
    intensity = Column(String(20), nullable=False)
    created_at= Column(DateTime, default=datetime.utcnow)
    updated_at= Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    plans     = relationship("WorkoutPlan", back_populates="user", cascade="all, delete-orphan")
    feedbacks = relationship("Feedback",    back_populates="user", cascade="all, delete-orphan")


class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id            = Column(Integer, primary_key=True, index=True)
    user_id       = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    original_plan = Column(Text, nullable=False)
    updated_plan  = Column(Text, nullable=True)
    nutrition_tip = Column(Text, nullable=True)
    created_at    = Column(DateTime, default=datetime.utcnow)
    updated_at    = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="plans")


class Feedback(Base):
    __tablename__ = "feedbacks"

    id            = Column(Integer, primary_key=True, index=True)
    user_id       = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    feedback_text = Column(Text, nullable=False)
    created_at    = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="feedbacks")

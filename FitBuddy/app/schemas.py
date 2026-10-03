from enum import Enum
from pydantic import BaseModel, field_validator


class GoalEnum(str, Enum):
    weight_loss      = "weight loss"
    muscle_gain      = "muscle gain"
    general_wellness = "general wellness"
    flexibility      = "flexibility"


class IntensityEnum(str, Enum):
    low    = "low"
    medium = "medium"
    high   = "high"


class UserInput(BaseModel):
    username:  str
    user_id:   int
    age:       int
    weight:    float
    goal:      GoalEnum
    intensity: IntensityEnum

    @field_validator("username")
    @classmethod
    def username_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Username cannot be empty.")
        return v.strip()

    @field_validator("age")
    @classmethod
    def age_range(cls, v):
        if not 10 <= v <= 100:
            raise ValueError("Age must be between 10 and 100.")
        return v

    @field_validator("weight")
    @classmethod
    def weight_positive(cls, v):
        if not 0 < v <= 500:
            raise ValueError("Weight must be between 0 and 500 kg.")
        return v


class FeedbackRequest(BaseModel):
    user_id:  int
    feedback: str

    @field_validator("feedback")
    @classmethod
    def feedback_length(cls, v):
        if len(v.strip()) < 5:
            raise ValueError("Feedback must be at least 5 characters.")
        return v.strip()


class AdminLogin(BaseModel):
    username: str
    password: str

from pydantic import BaseModel, Field


class UserInput(BaseModel):
    username: str = Field(min_length=1)
    user_id: str = Field(min_length=1)
    age: int = Field(ge=10, le=100)
    weight: float = Field(gt=0, le=400)
    goal: str
    intensity: str


class FeedbackRequest(BaseModel):
    user_id: str
    feedback: str = Field(min_length=1)

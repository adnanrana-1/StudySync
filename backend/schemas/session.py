from pydantic import BaseModel, Field
from datetime import datetime

class StudySessionCreateSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10, max_length=1000)
    subject: str = Field(..., min_length=2, max_length=50)
    location: str = Field(..., min_length=2, max_length=100)

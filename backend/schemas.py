from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User Schemas
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    major: str
    year: int  # 1, 2, 3, 4
    subjects: List[str]  # e.g., ["Math", "Physics"]
    bio: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserProfile(BaseModel):
    id: str
    name: str
    email: str
    major: str
    year: int
    subjects: List[str]
    bio: Optional[str]
    average_rating: Optional[float] = 0.0
    total_sessions: int = 0
    created_at: datetime

class UserUpdate(BaseModel):
    name: Optional[str] = None
    major: Optional[str] = None
    year: Optional[int] = None
    subjects: Optional[List[str]] = None
    bio: Optional[str] = None

# Session Schemas
class StudySessionCreate(BaseModel):
    title: str
    description: str
    subject: str
    date: str  # "2024-12-20"
    time: str  # "14:30"
    duration: int  # in minutes
    location: str  # online/offline or room name
    max_participants: int = 5

class StudySessionResponse(BaseModel):
    id: str
    title: str
    description: str
    subject: str
    date: str
    time: str
    duration: int
    location: str
    max_participants: int
    participants_count: int
    created_by: str
    created_at: datetime
    status: str  # "active", "completed", "cancelled"

class JoinSession(BaseModel):
    session_id: str

# Rating Schemas
class RatingCreate(BaseModel):
    to_user: str
    rating: int  # 1-5
    review: str

class RatingResponse(BaseModel):
    id: str
    from_user: str
    to_user: str
    rating: int
    review: str
    created_at: datetime

# Dashboard Schemas
class DashboardStats(BaseModel):
    total_sessions_attended: int
    total_sessions_hosted: int
    average_rating: float
    upcoming_sessions: int
    completed_sessions: int

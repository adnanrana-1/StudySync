import re
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, field_validator

class UserRegisterSchema(BaseModel):
    # This alias maps 'name' from incoming JSON directly into username
    username: str = Field(..., alias="name", min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    major: Optional[str] = ""
    year: Optional[int] = 1
    subjects: Optional[List[str]] = []
    bio: Optional[str] = ""

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one digit.")
        return v

    model_config = {
        "populate_by_name": True
    }

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserResponseSchema(BaseModel):
    id: str
    username: str
    email: str
    is_admin: bool = False

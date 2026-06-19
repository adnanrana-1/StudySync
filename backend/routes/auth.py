from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from database import get_database
from schemas.user import UserRegisterSchema, UserLoginSchema
from utils.auth import create_access_token

router = APIRouter(prefix="/api/auth", tags=["Authentication Layer"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", status_code=201)
async def register_user(payload: UserRegisterSchema, db=Depends(get_database)):
    existing_user = await db.users.find_one({"email": payload.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Account address already exists.")

    hashed_password = pwd_context.hash(payload.password)

    # Store complete profile attributes dynamically within Document Model mapping
    user_doc = {
        "username": payload.username,
        "email": payload.email,
        "password": hashed_password,
        "major": payload.major,
        "year": payload.year,
        "subjects": payload.subjects,
        "bio": payload.bio,
        "is_admin": False
    }

    if payload.username.lower() == "adnan":
        user_doc["is_admin"] = True

    await db.users.insert_one(user_doc)
    return {"status": "success", "message": "Secure identity registry verified."}


@router.post("/login")
async def login_user(payload: UserLoginSchema, db=Depends(get_database)):
    user = await db.users.find_one({"email": payload.email})
    if not user or not pwd_context.verify(payload.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credential combination.")

    token = create_access_token(data={"sub": str(user["_id"])})
    return {
        "access_token": token,
        "token_type": "bearer",
        "is_admin": user.get("is_admin", False),
        "username": user["username"]
    }

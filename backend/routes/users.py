from fastapi import APIRouter, HTTPException, status, Header
from bson.objectid import ObjectId
from schemas import UserProfile, UserUpdate
from database import users_collection, study_sessions_collection, ratings_collection
from datetime import datetime
import jwt
from config import settings

router = APIRouter(prefix="/api/users", tags=["users"])


def get_current_user(authorization: str = Header(None)):
    """Extract user from JWT token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        return user_id
    except:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/profile/{user_id}")
async def get_user_profile(user_id: str):
    """Get user profile"""
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Calculate stats
        sessions_hosted = study_sessions_collection.count_documents({"created_by": user_id})
        sessions_participated = study_sessions_collection.count_documents(
            {"participants": {"$in": [user_id]}}
        )

        ratings = list(ratings_collection.find({"to_user": user_id}))
        avg_rating = sum([r["rating"] for r in ratings]) / len(ratings) if ratings else 0

        return {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "major": user["major"],
            "year": user["year"],
            "subjects": user["subjects"],
            "bio": user.get("bio", ""),
            "average_rating": round(avg_rating, 1),
            "total_sessions_hosted": sessions_hosted,
            "total_sessions_participated": sessions_participated,
            "created_at": user["created_at"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/profile/{user_id}")
async def update_user_profile(user_id: str, update_data: UserUpdate):
    """Update user profile"""
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        update_dict = {k: v for k, v in update_data.dict().items() if v is not None}

        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_dict}
        )

        return {"message": "Profile updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
async def search_users(subject: str, year: int = None, major: str = None):
    """Search study partners by subject"""
    try:
        query = {"subjects": {"$in": [subject]}}

        if year:
            query["year"] = year
        if major:
            query["major"] = major

        users = list(users_collection.find(query).limit(20))

        result = []
        for user in users:
            ratings = list(ratings_collection.find({"to_user": str(user["_id"])}))
            avg_rating = sum([r["rating"] for r in ratings]) / len(ratings) if ratings else 0

            result.append({
                "id": str(user["_id"]),
                "name": user["name"],
                "major": user["major"],
                "year": user["year"],
                "subjects": user["subjects"],
                "bio": user.get("bio", ""),
                "average_rating": round(avg_rating, 1)
            })

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
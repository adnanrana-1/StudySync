from fastapi import APIRouter, HTTPException, Header
from bson.objectid import ObjectId
from schemas import RatingCreate
from database import ratings_collection, users_collection
from datetime import datetime
import jwt
from config import settings

router = APIRouter(prefix="/api/ratings", tags=["ratings"])


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


@router.post("/create")
async def create_rating(rating: RatingCreate, authorization: str = Header(None)):
    """Rate a study partner"""
    try:
        from_user = get_current_user(authorization)

        # Check if already rated
        existing = ratings_collection.find_one({
            "from_user": from_user,
            "to_user": rating.to_user
        })

        if existing:
            raise HTTPException(status_code=400, detail="Already rated this user")

        rating_doc = {
            "from_user": from_user,
            "to_user": rating.to_user,
            "rating": rating.rating,
            "review": rating.review,
            "created_at": datetime.utcnow()
        }

        result = ratings_collection.insert_one(rating_doc)

        return {
            "message": "Rating submitted successfully",
            "rating_id": str(result.inserted_id)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/{user_id}")
async def get_user_ratings(user_id: str):
    """Get all ratings for a user"""
    try:
        ratings = list(ratings_collection.find({"to_user": user_id}))

        result = []
        for rating in ratings:
            rater = users_collection.find_one({"_id": ObjectId(rating["from_user"])})

            result.append({
                "id": str(rating["_id"]),
                "from_user_name": rater["name"] if rater else "Unknown",
                "rating": rating["rating"],
                "review": rating["review"],
                "created_at": rating["created_at"]
            })

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

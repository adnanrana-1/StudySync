import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from bson import ObjectId
from database import get_database
from schemas.session import StudySessionCreateSchema
from utils.auth import get_current_user

router = APIRouter(prefix="/api/sessions", tags=["Sessions Engine Layer"])


@router.get("/all")
async def fetch_all_paginated_sessions(
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=50),
        db=Depends(get_database)
):
    skip = (page - 1) * limit

    pipeline = [
        {"$skip": skip},
        {"$limit": limit},
        {
            "$lookup": {
                "from": "users",
                "let": {"creator_oid": {"$toObjectId": "$creator_id"}},
                "pipeline": [
                    {"$match": {"$expr": {"$eq": ["$_id", "$$creator_oid"]}}}
                ],
                "as": "creator_info"
            }
        },
        {"$unwind": {"path": "$creator_info", "preserveNullAndEmptyArrays": True}}
    ]

    cursor = db.sessions.aggregate(pipeline)
    sessions_list = await cursor.to_list(length=limit)

    formatted = []
    for s in sessions_list:
        formatted.append({
            "id": str(s["_id"]),
            "title": s["title"],
            "description": s["description"],
            "subject": s["subject"],
            "location": s["location"],
            "created_at": s.get("created_at"),
            "creator_id": s.get("creator_id"),
            "creator_name": s.get("creator_info", {}).get("username", "System Sync")
        })
    return formatted


@router.post("/create", status_code=201)
async def instantiate_session(
        payload: StudySessionCreateSchema,
        current_user: dict = Depends(get_current_user),
        db=Depends(get_database)
):
    session_doc = payload.model_dump()
    session_doc["creator_id"] = current_user["id"]
    session_doc["created_at"] = datetime.datetime.utcnow()

    result = await db.sessions.insert_one(session_doc)
    return {"status": "success", "session_id": str(result.inserted_id)}


@router.delete("/delete/{session_id}")
async def wipe_session_record(
        session_id: str,
        current_user: dict = Depends(get_current_user),
        db=Depends(get_database)
):
    try:
        oid = ObjectId(session_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid target entity coordinate signature format.")

    target_session = await db.sessions.find_one({"_id": oid})
    if not target_session:
        raise HTTPException(status_code=404, detail="Target document node non-existent.")

    is_owner = target_session.get("creator_id") == current_user["id"]
    is_admin = current_user.get("is_admin", False)

    if not is_owner and not is_admin:
        raise HTTPException(status_code=403, detail="Operational access permissions rejected.")

    await db.sessions.delete_one({"_id": oid})
    return {"status": "success", "message": "Cluster instance document deleted safely."}

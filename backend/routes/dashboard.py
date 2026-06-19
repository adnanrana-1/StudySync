from fastapi import APIRouter, Depends
from database import get_database

router = APIRouter(prefix="/api/dashboard", tags=["Metrics Engine"])

@router.get("/stats")
async def collect_system_metrics(db=Depends(get_database)):
    total_sessions = await db.sessions.count_documents({})
    return {
        "active_sessions": total_sessions,
        "active_sessions_badge": "Live Engine",
        "ratings": 4.8,
        "study_hours": "142h Cumulative",
        "study_hours_badge": "Production Level"
    }

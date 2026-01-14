from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, timedelta
import uuid

from services.sheets import get_sheet

router = APIRouter(prefix="/session", tags=["Session"])

@router.post("/create")
def create_session(class_id: str = Query(...)):
    try:
        sessions_sheet = get_sheet("Sessions")

        session_id = str(uuid.uuid4())
        now = datetime.now()
        end_time = now + timedelta(minutes=5)

        sessions_sheet.append_row([
            session_id,
            class_id,
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M"),
            end_time.strftime("%H:%M"),
            "YES"
        ])

        return {
            "session_id": session_id,
            "class_id": class_id,
            "expires_at": end_time.isoformat()
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Session creation failed: {str(e)}"
        )

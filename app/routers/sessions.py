from fastapi import APIRouter
from datetime import datetime, timedelta
import uuid
from app.services.sheets import get_worksheet

router = APIRouter(prefix="/session", tags=["Session"])

SHEET_NAME = "Attendance_MVP_Database"

@router.post("/create")
def create_session(class_id: str):
    ws = get_worksheet(SHEET_NAME, "Sessions")

    session_id = str(uuid.uuid4())
    start = datetime.now()
    end = start + timedelta(minutes=5)

    ws.append_row([
        session_id,
        class_id,
        start.strftime("%Y-%m-%d"),
        start.strftime("%H:%M"),
        end.strftime("%H:%M"),
        "YES"
    ])

    return {
        "session_id": session_id,
        "expires_at": end.isoformat()
    }
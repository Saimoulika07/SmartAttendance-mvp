from fastapi import APIRouter
from datetime import datetime, timedelta
import uuid
from database import conn, cursor

router = APIRouter(prefix="/session")

@router.post("/create")
def create_session(class_id: str):
    session_id = str(uuid.uuid4())
    start = datetime.now()
    end = start + timedelta(minutes=5)

    cursor.execute(
        "INSERT INTO sessions VALUES (?, ?, ?, ?, ?)",
        (session_id, class_id, start.isoformat(), end.isoformat(), 1)
    )
    conn.commit()

    return {
        "session_id": session_id,
        "expires_at": end.isoformat()
    }

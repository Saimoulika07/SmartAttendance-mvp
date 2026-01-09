from fastapi import APIRouter, HTTPException
from datetime import datetime
from database import conn, cursor

router = APIRouter(prefix="/attendance")

@router.post("/mark")
def mark_attendance(session_id: str, student_email: str):
    cursor.execute(
        "SELECT end_time, active FROM sessions WHERE session_id=?",
        (session_id,)
    )
    row = cursor.fetchone()
    if not row or row[1] == 0:
        raise HTTPException(status_code=400, detail="Invalid session")

    if datetime.now().isoformat() > row[0]:
        raise HTTPException(status_code=400, detail="Session expired")

    try:
        cursor.execute(
            "INSERT INTO attendance (session_id, student_email, timestamp) VALUES (?, ?, ?)",
            (session_id, student_email, datetime.now().isoformat())
        )
        conn.commit()
    except:
        raise HTTPException(status_code=400, detail="Attendance already marked")

    return {"status": "Attendance marked"}

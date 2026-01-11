from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.services.sheets import get_worksheet

router = APIRouter(prefix="/attendance", tags=["Attendance"])

SHEET_NAME = "Attendance_MVP_Database"

@router.post("/mark")
def mark_attendance(session_id: str, student_email: str):
    sessions_ws = get_worksheet(SHEET_NAME, "Sessions")
    attendance_ws = get_worksheet(SHEET_NAME, "Attendance")

    sessions = sessions_ws.get_all_records()
    session = next((s for s in sessions if s["SessionID"] == session_id), None)

    if not session or session["Active"] != "YES":
        raise HTTPException(status_code=400, detail="Invalid session")

    if datetime.now().strftime("%H:%M") > session["EndTime"]:
        raise HTTPException(status_code=400, detail="Session expired")

    records = attendance_ws.get_all_records()
    for r in records:
        if r["SessionID"] == session_id and r["StudentEmail"] == student_email:
            raise HTTPException(status_code=400, detail="Already marked")

    attendance_ws.append_row([
        session["Date"],
        session["ClassID"],
        session_id,
        student_email,
        datetime.now().isoformat(),
        "Present"
    ])

    return {"status": "Attendance marked"}

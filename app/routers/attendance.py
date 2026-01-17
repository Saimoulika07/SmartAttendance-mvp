from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from app.services.sheets import get_sheet

router = APIRouter(prefix="/attendance", tags=["Attendance"])

class AttendanceRequest(BaseModel):
    session_id: str
    student_email: str

@router.post("/mark")
def mark_attendance(data: AttendanceRequest):
    sheet = get_sheet("Attendance")
    records = sheet.get_all_records()

    # 🔒 DUPLICATE CHECK
    for row in records:
        if (
            row.get("session_id") == data.session_id
            and row.get("student_email") == data.student_email
        ):
            raise HTTPException(
                status_code=400,
                detail="Attendance already marked for this session"
            )

    # ✅ If not duplicate, mark attendance
    sheet.append_row([
        data.session_id,
        data.student_email,
        datetime.utcnow().isoformat(),
        "PRESENT",
        ""  # class_id if auto-filled later
    ])

    return {
        "message": "Attendance marked successfully",
        "session_id": data.session_id,
        "student_email": data.student_email
    }
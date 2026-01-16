from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.services.sheets import get_sheet

router = APIRouter(prefix="/attendance", tags=["Attendance"])

@router.post("/mark")
def mark_attendance(
    session_id: str,
    student_email: str
):
    try:
        sheet = get_sheet("Attendance")

        sheet.append_row([
            session_id,
            student_email,
            datetime.utcnow().isoformat(),
            "PRESENT"
        ])

        return {
            "message": "Attendance marked",
            "session_id": session_id,
            "student_email": student_email
        }

    except Exception as e:
        print("ATTENDANCE ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))

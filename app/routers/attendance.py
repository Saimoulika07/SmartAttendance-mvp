from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.services.sheets import get_sheet

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("/mark")
def mark_attendance(session_id: str, student_email: str):
    try:
        attendance_sheet = get_sheet("Attendance")
        sessions_sheet = get_sheet("Sessions")

        # 🔹 Fetch all sessions
        sessions = sessions_sheet.get_all_records()
        session = next(
            (s for s in sessions if s.get("session_id") == session_id),
            None
        )

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        # 🔹 Check expiry (QR time window)
        expiry_time = session.get("expiry_time")
        if expiry_time:
            expiry = datetime.fromisoformat(expiry_time)
            if datetime.utcnow() > expiry:
                raise HTTPException(
                    status_code=400,
                    detail="Attendance window closed"
                )

        # 🔹 Prevent duplicate attendance
        records = attendance_sheet.get_all_records()
        for row in records:
            if (
                row.get("session_id") == session_id
                and row.get("student_email") == student_email
            ):
                raise HTTPException(
                    status_code=400,
                    detail="Attendance already marked for this session"
                )

        # 🔹 Mark attendance
        attendance_sheet.append_row([
            session_id,
            student_email,
            datetime.utcnow().isoformat(),
            "PRESENT",
            session.get("class_id", "")
        ])

        return {
            "message": "Attendance marked successfully",
            "session_id": session_id,
            "student_email": student_email
        }

    except HTTPException:
        raise
    except Exception as e:
        print("ATTENDANCE ERROR:", e)
        raise HTTPException(status_code=500, detail="Internal server error")

from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.services.sheets import get_sheet

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("/mark")
def mark_attendance(session_id: str, student_email: str):
    try:
        attendance_sheet = get_sheet("Attendance")
        sessions_sheet = get_sheet("Sessions")

        # 🔹 Fetch sessions ONCE
        sessions = sessions_sheet.get_all_records()
        session_map = {s["session_id"]: s for s in sessions}

        session = session_map.get(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        # 🔹 Expiry check (QR window)
        expiry_time = session.get("expiry_time")
        if expiry_time:
            if datetime.utcnow() > datetime.fromisoformat(expiry_time):
                raise HTTPException(
                    status_code=400,
                    detail="Attendance window closed"
                )

        # 🔹 Prevent duplicates (single pass)
        records = attendance_sheet.get_all_records()
        for row in records:
            if (
                row["session_id"] == session_id
                and row["student_email"] == student_email
            ):
                raise HTTPException(
                    status_code=400,
                    detail="Attendance already marked"
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
            "status": "success",
            "session_id": session_id,
            "student": student_email,
            "marked_at": datetime.utcnow().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        print("ATTENDANCE ERROR:", e)
        raise HTTPException(status_code=500, detail="Internal server error")

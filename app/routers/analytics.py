from fastapi import APIRouter, Query
from collections import defaultdict
from app.services.sheets import get_sheet

router = APIRouter(prefix="/analytics", tags=["Analytics"])


# ---------- KEEP EXISTING EXPORT ----------
@router.get("/export")
def export_analytics():
    attendance = get_sheet("Attendance").get_all_values()
    sessions = get_sheet("Sessions").get_all_values()

    return {
        "attendance_rows": attendance,
        "sessions_rows": sessions
    }


# ---------- STUDENT ANALYTICS ----------
@router.get("/student")
def student_analytics(
    student_email: str = Query(..., description="Student email")
):
    attendance = get_sheet("Attendance").get_all_values()
    sessions = get_sheet("Sessions").get_all_values()

    if not attendance or not sessions:
        return {
            "student_email": student_email,
            "total_sessions": 0,
            "attended_sessions": 0,
            "attendance_percentage": 0,
            "subject_wise": []
        }

    # session_id → subject_code
    session_subject = {}
    for row in sessions[1:]:
        if len(row) >= 6:
            session_subject[row[0]] = row[5]

    total_sessions = len(session_subject)
    attended_sessions = 0
    subject_stats = defaultdict(lambda: {"attended": 0, "total": 0})

    for subject in session_subject.values():
        subject_stats[subject]["total"] += 1

    for row in attendance[1:]:
        if len(row) >= 4 and row[1] == student_email and row[3] == "PRESENT":
            attended_sessions += 1
            subject = session_subject.get(row[0])
            if subject:
                subject_stats[subject]["attended"] += 1

    subject_wise = []
    for subject, stats in subject_stats.items():
        percent = round(
            (stats["attended"] / stats["total"]) * 100, 2
        ) if stats["total"] else 0

        subject_wise.append({
            "subject_code": subject,
            "attended": stats["attended"],
            "total": stats["total"],
            "percentage": percent
        })

    overall_percentage = round(
        (attended_sessions / total_sessions) * 100, 2
    ) if total_sessions else 0

    return {
        "student_email": student_email,
        "total_sessions": total_sessions,
        "attended_sessions": attended_sessions,
        "attendance_percentage": overall_percentage,
        "subject_wise": subject_wise
    }

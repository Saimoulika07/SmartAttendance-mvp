from fastapi import APIRouter, Query
from collections import defaultdict
from app.services.sheets import get_sheet

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/student")
def student_analytics(student_email: str = Query(...)):
    attendance = get_sheet("Attendance").get_all_records()
    sessions = get_sheet("Sessions").get_all_records()

    session_subject = {
        s["session_id"]: s.get("subject_code")
        for s in sessions
    }

    subject_stats = defaultdict(lambda: {"attended": 0, "total": 0})

    # total classes per subject
    for subject in session_subject.values():
        if subject:
            subject_stats[subject]["total"] += 1

    attended_sessions = 0
    for row in attendance:
        if row["student_email"] == student_email and row["status"] == "PRESENT":
            attended_sessions += 1
            subject = session_subject.get(row["session_id"])
            if subject:
                subject_stats[subject]["attended"] += 1

    total_sessions = len(session_subject)
    percentage = round((attended_sessions / total_sessions) * 100, 2) if total_sessions else 0

    return {
        "student_email": student_email,
        "attendance_percentage": percentage,
        "subject_wise": subject_stats
    }


@router.get("/faculty")
def faculty_analytics(class_id: str, subject_code: str):
    attendance = get_sheet("Attendance").get_all_records()
    sessions = get_sheet("Sessions").get_all_records()

    relevant_sessions = {
        s["session_id"]
        for s in sessions
        if s["class_id"] == class_id and s["subject_code"] == subject_code
    }

    student_presence = defaultdict(set)

    for row in attendance:
        if row["session_id"] in relevant_sessions:
            student_presence[row["student_email"]].add(row["session_id"])

    total_students = len(student_presence)
    total_sessions = len(relevant_sessions)

    present_count = sum(
        1 for v in student_presence.values()
        if len(v) == total_sessions
    )

    percentage = round((present_count / total_students) * 100, 2) if total_students else 0

    return {
        "class_id": class_id,
        "subject_code": subject_code,
        "total_students": total_students,
        "attendance_percentage": percentage
    }


@router.get("/at-risk")
def at_risk_students(threshold: int = 75):
    attendance = get_sheet("Attendance").get_all_records()
    sessions = get_sheet("Sessions").get_all_records()

    total_sessions = len(sessions)
    student_attendance = defaultdict(int)

    for row in attendance:
        if row["status"] == "PRESENT":
            student_attendance[row["student_email"]] += 1

    at_risk = []
    for student, attended in student_attendance.items():
        percentage = (attended / total_sessions) * 100 if total_sessions else 0
        if percentage < threshold:
            at_risk.append({
                "student_email": student,
                "attendance_percentage": round(percentage, 2)
            })

    return {
        "threshold": threshold,
        "at_risk_students": at_risk
    }

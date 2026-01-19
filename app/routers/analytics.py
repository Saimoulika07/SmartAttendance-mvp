from fastapi import APIRouter, Query
from collections import defaultdict
from app.services.sheets import get_sheet

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/student")
def student_analytics(student_email: str = Query(...)):
    attendance = get_sheet("Attendance").get_all_values()
    sessions = get_sheet("Sessions").get_all_values()

    session_subject = {}
    for row in sessions[1:]:
        session_subject[row[0]] = row[5]  # session_id → subject_code

    subject_stats = defaultdict(lambda: {"attended": 0, "total": 0})

    for subject in session_subject.values():
        subject_stats[subject]["total"] += 1

    attended_sessions = 0
    for row in attendance[1:]:
        if row[1] == student_email and row[3] == "PRESENT":
            attended_sessions += 1
            subject = session_subject.get(row[0])
            if subject:
                subject_stats[subject]["attended"] += 1

    total_sessions = len(session_subject)
    percentage = round((attended_sessions / total_sessions) * 100, 2) if total_sessions else 0

    return {
        "student_email": student_email,
        "total_sessions": total_sessions,
        "attended_sessions": attended_sessions,
        "attendance_percentage": percentage,
        "subject_wise": [
            {
                "subject": k,
                "attended": v["attended"],
                "total": v["total"]
            }
            for k, v in subject_stats.items()
        ]
    }


@router.get("/faculty")
def faculty_analytics(class_id: str, subject_code: str):
    attendance = get_sheet("Attendance").get_all_values()
    sessions = get_sheet("Sessions").get_all_values()

    relevant_sessions = [
        row[0] for row in sessions[1:]
        if row[1] == class_id and row[5] == subject_code
    ]

    students = set()
    present = 0

    for row in attendance[1:]:
        if row[0] in relevant_sessions:
            students.add(row[1])
            if row[3] == "PRESENT":
                present += 1

    total = len(students)
    absent = max(total - present, 0)
    percentage = round((present / total) * 100, 2) if total else 0

    return {
        "class_id": class_id,
        "subject_code": subject_code,
        "total_students": total,
        "present": present,
        "absent": absent,
        "attendance_percentage": percentage
    }

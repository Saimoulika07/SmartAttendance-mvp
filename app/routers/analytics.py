from fastapi import APIRouter
from app.services.sheets import get_sheet

router = APIRouter(prefix="/analytics", tags=["Analytics"])

SHEET_NAME = "Attendance_MVP_Database"

@router.post("/export")
def export_analytics():
    attendance_ws = get_sheet(SHEET_NAME, "Attendance")
    analytics_ws = get_sheet(SHEET_NAME, "Analytics")

    records = attendance_ws.get_all_records()

    counts = {}
    for r in records:
        sid = r["SessionID"]
        counts[sid] = counts.get(sid, 0) + 1

    analytics_ws.clear()
    analytics_ws.append_row(["SessionID", "PresentCount"])

    for sid, count in counts.items():
        analytics_ws.append_row([sid, count])

    return {"status": "Analytics exported"}

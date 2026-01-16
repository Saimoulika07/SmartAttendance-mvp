from fastapi import APIRouter, HTTPException
from app.services.sheets import get_sheet

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/export")
def export_analytics():
    try:
        attendance_sheet = get_sheet("Attendance")
        rows = attendance_sheet.get_all_records()

        return {
            "total_records": len(rows),
            "data": rows
        }

    except Exception as e:
        print("ANALYTICS ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))

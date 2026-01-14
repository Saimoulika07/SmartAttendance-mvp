from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, timedelta
import uuid
import os

from database import get_db_connection
from app.services.sheets import get_gspread_client

router = APIRouter(prefix="/session", tags=["Session"])


@router.post("/create")
def create_session(class_id: str = Query(..., description="Class ID")):
    session_id = str(uuid.uuid4())
    start_time = datetime.utcnow()
    end_time = start_time + timedelta(minutes=5)

    # ---------- 1. Save to SQLite ----------
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO sessions (session_id, class_id, start_time, end_time, active)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                session_id,
                class_id,
                start_time.isoformat(),
                end_time.isoformat(),
                "YES",
            ),
        )

        conn.commit()
        conn.close()

    except Exception as e:
        print("🔥 SQLITE ERROR:", str(e))
        raise HTTPException(status_code=500, detail="Database error")

    # ---------- 2. Save to Google Sheets ----------
    try:
        client = get_gspread_client()

        sheet_id = os.environ.get("GOOGLE_SHEET_ID")
        if not sheet_id:
            raise Exception("GOOGLE_SHEET_ID not set")

        sheet = client.open_by_key(sheet_id)

        # ⚠️ SHEET NAME MUST MATCH EXACTLY
        worksheet = sheet.worksheet("Sessions")

        worksheet.append_row(
            [
                session_id,
                class_id,
                start_time.date().isoformat(),
                start_time.time().strftime("%H:%M:%S"),
                end_time.time().strftime("%H:%M:%S"),
                "YES",
            ]
        )

    except Exception as e:
        print("🔥 GOOGLE SHEETS ERROR:", str(e))
        raise HTTPException(status_code=500, detail="Google Sheets error")

    # ---------- 3. Success ----------
    return {
        "message": "Session created",
        "session_id": session_id,
        "class_id": class_id,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
    }

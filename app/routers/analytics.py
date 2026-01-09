from fastapi import APIRouter
import sqlite3
import gspread
from google.oauth2.service_account import Credentials

router = APIRouter(prefix="/analytics")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SPREADSHEET_ID = "1Q0Ta9Q79GCy85HZL0ew3T3Cm3uORJgllLc6WJTn9m1c"

@router.post("/export")
def export_attendance():
    conn = sqlite3.connect("attendance.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT session_id, COUNT(*) 
        FROM attendance 
        GROUP BY session_id
    """)
    data = cur.fetchall()

    creds = Credentials.from_service_account_file(
        "service_account.json",
        scopes=SCOPES
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet("Analytics")

    sheet.clear()
    sheet.append_row(["SessionID", "PresentCount"])

    for row in data:
        sheet.append_row(list(row))

    return {"status": "Exported to Google Sheets"}

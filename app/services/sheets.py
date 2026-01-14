import os
import json
import gspread
from google.oauth2.service_account import Credentials

_client = None

def get_gspread_client():
    global _client

    if _client:
        return _client

    raw = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not raw:
        raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_JSON not set")

    try:
        service_account_info = json.loads(raw)
    except Exception as e:
        raise RuntimeError(f"Invalid service account JSON: {e}")

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        service_account_info,
        scopes=scopes
    )

    _client = gspread.authorize(creds)
    return _client


def get_sheet(sheet_name: str):
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    if not sheet_id:
        raise RuntimeError("GOOGLE_SHEET_ID not set")

    client = get_gspread_client()
    return client.open_by_key(sheet_id).worksheet(sheet_name)

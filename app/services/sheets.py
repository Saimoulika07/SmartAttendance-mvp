import os
import json
import gspread
from google.oauth2.service_account import Credentials

def get_sheet(sheet_name: str):
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    if not sheet_id:
        raise Exception("GOOGLE_SHEET_ID not set")

    service_account_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not service_account_json:
        raise Exception("GOOGLE_SERVICE_ACCOUNT_JSON not set")

    creds_dict = json.loads(service_account_json)

    creds = Credentials.from_service_account_info(
        creds_dict,
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
    )

    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(sheet_id)

    return spreadsheet.worksheet(sheet_name)
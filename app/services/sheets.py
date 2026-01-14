import os
import json
import gspread
from google.oauth2.service_account import Credentials

def get_gspread_client():
    service_account_info = json.loads(
        os.environ.get["GOOGLE_SERVICE_ACCOUNT_JSON"]
    )

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        service_account_info, scopes=scopes
    )

    return gspread.authorize(creds)
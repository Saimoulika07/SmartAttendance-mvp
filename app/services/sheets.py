import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_worksheet(sheet_name: str, tab_name: str):
    creds = Credentials.from_service_account_file(
        "service_account.json",
        scopes=SCOPES
    )
    client = gspread.authorize(creds)
    return client.open(sheet_name).worksheet(tab_name)
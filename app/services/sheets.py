import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SPREADSHEET_ID = "1Q0Ta9Q79GCy85HZL0ew3T3Cm3uORJgllLc6WJTn9m1c"

_client = None
_spreadsheet = None

def get_sheet(worksheet_name: str):
    global _client, _spreadsheet

    if _client is None:
        creds = Credentials.from_service_account_file(
            "service_account.json",
            scopes=SCOPES
        )
        _client = gspread.authorize(creds)
        _spreadsheet = _client.open_by_key(SPREADSHEET_ID)

    return _spreadsheet.worksheet(worksheet_name)

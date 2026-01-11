# Smart Attendance MVP

Backend MVP for a QR-based smart attendance system with session control and analytics.

## Tech Stack
- FastAPI (Python)
- SQLite (local database)
- Google Sheets (data sync & analytics source)
- Looker Studio (dashboard)

## Features
- Create attendance sessions
- Mark attendance using session ID
- Prevent duplicate attendance
- Store data in SQLite
- Sync data to Google Sheets
- Basic analytics export

## Project Structure
- app/routers → API routes (sessions, attendance, analytics)
- app/services → Google Sheets integration
- database.py → SQLite setup
- main.py → FastAPI entry point

## How to Run Locally
1. Clone the repository
2. Create and activate virtual environment
3. Install dependencies:
pip install -r requirements.txt
4. Add Google service account key:
- Place `service_account.json` in root
5. Run the server:
python -m uvicorn main:app --reload
6. Open API docs:
http://127.0.0.1:8000/docs


## Notes
- This is a backend MVP.
- Frontend and deployment will be added next.
- Analytics dashboard is built using Google Looker Studio.

## Author
Sai Moulika

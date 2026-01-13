# Smart Attendance MVP

Backend for QR-based attendance system built with FastAPI.

## Features
- Session creation
- Attendance marking
- Google Sheets integration
- Analytics export
- Swagger API docs

## Tech Stack
- FastAPI
- SQLite
- Google Sheets API
- Render (deployment)

## Live API
Backend is deployed on Render.
Swagger UI available at `/docs`.

## Run locally
```bash
pip install -r requirements.txt
uvicorn main:app --reload
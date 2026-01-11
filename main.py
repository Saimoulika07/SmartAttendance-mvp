from fastapi import FastAPI
from app.routers import sessions, attendance, analytics

app = FastAPI(title="Attendance MVP")

app.include_router(sessions.router)
app.include_router(attendance.router)
app.include_router(analytics.router)

@app.get("/")
def root():
    return {"status": "Backend running"}

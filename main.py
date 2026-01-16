from fastapi import FastAPI
from app.routers import sessions, attendance, analytics

app = FastAPI()

app.include_router(sessions.router)
app.include_router(attendance.router)
app.include_router(analytics.router)

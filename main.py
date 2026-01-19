from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import sessions, attendance, analytics

# CREATE APP FIRST
app = FastAPI(title="Smart Attendance MVP")

# ADD CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# INCLUDE ROUTERS
app.include_router(sessions.router)
app.include_router(attendance.router)
app.include_router(analytics.router)

# ROOT CHECK
@app.get("/")
def root():
    return {"status": "Backend running"}

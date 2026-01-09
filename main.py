from fastapi import FastAPI
from app.routers import attendance, sessions
from app.routers import analytics


app = FastAPI(title="Attendance MVP API")

app.include_router(sessions.router)
app.include_router(attendance.router)
app.include_router(analytics.router)

@app.get("/")
def root():
    return {"status": "Backend running successfully"}
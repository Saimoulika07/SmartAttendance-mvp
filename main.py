from fastapi import FastAPI
from app.routers import sessions, attendance, analytics
import os

app = FastAPI(title="Attendance MVP")

app.include_router(sessions.router)
app.include_router(attendance.router)
app.include_router(analytics.router)

@app.get("/")
def root():
    return {"status": "Backend running"}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )

from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, timedelta
import uuid
from app.services.sheets import get_sheet

router = APIRouter(prefix="/session", tags=["Session"])

@router.post("/create")
def create_session(class_id: str = Query(...)):
    try:
        sheet = get_sheet("Sessions")

        session_id = str(uuid.uuid4())
        now = datetime.utcnow()

        # 🔒 Timed QR expiry (5 minutes)
        expiry_time = now + timedelta(minutes=5)

        sheet.append_row([
            session_id,
            class_id,
            now.isoformat(),
            expiry_time.isoformat()
        ])

        return {
            "session_id": session_id,
            "class_id": class_id,
            "expires_at": expiry_time.isoformat()
        }

    except Exception as e:
        print("SESSION ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))

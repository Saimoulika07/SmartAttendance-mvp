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
        end_time = now + timedelta(hours=1)

        sheet.append_row([
            session_id,
            class_id,
            now.isoformat(),
            end_time.isoformat()
        ])

        return {
            "session_id": session_id,
            "class_id": class_id,
            "expires_at": end_time.isoformat()
        }

    except Exception as e:
        print("SESSION ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))

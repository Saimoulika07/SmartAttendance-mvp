from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
import uuid
from app.services.sheets import get_sheet

router = APIRouter(prefix="/session", tags=["Sessions"])


@router.post("/create")
def create_session(class_id: str, subject_code: str):
    try:
        sheet = get_sheet("Sessions")

        session_id = str(uuid.uuid4())
        created_at = datetime.utcnow()
        expiry_time = created_at + timedelta(minutes=5)

        sheet.append_row([
            session_id,
            class_id,
            created_at.isoformat(),
            expiry_time.isoformat(),
            subject_code
        ])

        return {
            "session_id": session_id,
            "class_id": class_id,
            "subject_code": subject_code,
            "expires_at": expiry_time.isoformat()
        }

    except Exception as e:
        print("SESSION ERROR:", e)
        raise HTTPException(status_code=500, detail="Failed to create session")

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Module, AttendanceSession
from app.schemas import CreateSessionReq, CreateSessionRes
from app.core.config import settings
from app.core.security import create_short_token

router = APIRouter(prefix="/api/lecturer", tags=["lecturer"])

@router.post("/session", response_model=CreateSessionRes)
def create_session(req: CreateSessionReq, db: Session = Depends(get_db)):
    module = db.query(Module).filter(Module.code == req.module_code).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    s = AttendanceSession(module_id=module.id, active=True)
    db.add(s)
    db.commit()
    db.refresh(s)
    return {"session_id": s.id}

@router.get("/session/{session_id}/token")
def session_token(session_id: int, db: Session = Depends(get_db)):
    s = db.query(AttendanceSession).filter(AttendanceSession.id == session_id, AttendanceSession.active == True).first()
    if not s:
        raise HTTPException(status_code=404, detail="Session not active")
    token = create_short_token(settings.JWT_SECRET, session_id=session_id, ttl_seconds=10)
    url = f"{settings.APP_BASE_URL}/s/{session_id}?t={token}"
    return {"token": token, "url": url, "ttl": 10}

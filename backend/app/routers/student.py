from fastapi import APIRouter, Depends, Request, HTTPException, Response
from sqlalchemy.orm import Session
import uuid

from app.db.session import get_db
from app.db.models import Student, AttendanceSession, Attendance
from app.schemas import StudentLookupRes, MarkAttendanceReq, MarkAttendanceRes
from app.core.config import settings
from app.core.security import decode_token
from app.core.wifi_guard import enforce_wifi_only, get_client_ip
from app.utils.device import device_hash

router = APIRouter(prefix="/api/student", tags=["student"])

@router.get("/device")
def ensure_device_cookie(response: Response, request: Request):
    # sets device_id cookie if not exists
    device_id = request.cookies.get("device_id")
    if not device_id:
        device_id = str(uuid.uuid4())
        response.set_cookie("device_id", device_id, httponly=False, samesite="Lax", max_age=60*60*24*365)
    return {"device_id": device_id}

@router.get("/lookup/{reg_no}", response_model=StudentLookupRes)
def lookup(reg_no: str, request: Request, db: Session = Depends(get_db)):
    enforce_wifi_only(request)
    st = db.query(Student).filter(Student.reg_no == reg_no).first()
    if not st:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"reg_no": st.reg_no, "name": st.name, "index_no": st.index_no}

@router.post("/mark", response_model=MarkAttendanceRes)
def mark(req: MarkAttendanceReq, request: Request, db: Session = Depends(get_db)):
    enforce_wifi_only(request)

    # token validate
    try:
        payload = decode_token(settings.JWT_SECRET, req.token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid/Expired QR token")

    sid = int(payload.get("sid", -1))
    session = db.query(AttendanceSession).filter(AttendanceSession.id == sid, AttendanceSession.active == True).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not active")

    st = db.query(Student).filter(Student.reg_no == req.reg_no).first()
    if not st:
        raise HTTPException(status_code=404, detail="Student not found")

    device_id = request.cookies.get("device_id") or "no-cookie"
    ua = request.headers.get("user-agent", "")
    d_hash = device_hash(device_id, ua)
    ip = get_client_ip(request)

    att = Attendance(session_id=sid, student_id=st.id, device_hash=d_hash, ip=ip)
    db.add(att)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=409, detail="Already marked (student or device)")

    return {"status": "OK - Attendance marked"}

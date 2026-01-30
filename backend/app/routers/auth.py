from fastapi import APIRouter, HTTPException
from app.schemas import LoginReq, LoginRes
from app.core.config import settings

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login", response_model=LoginRes)
def login(req: LoginReq):
    if req.password != settings.LECTURER_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid password")
    return {"ok": True}

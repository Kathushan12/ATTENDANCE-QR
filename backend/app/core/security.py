from datetime import datetime, timedelta, timezone
from jose import jwt

ALGO = "HS256"

def create_short_token(secret: str, session_id: int, ttl_seconds: int = 10) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sid": session_id,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=ttl_seconds)).timestamp()),
    }
    return jwt.encode(payload, secret, algorithm=ALGO)

def decode_token(secret: str, token: str) -> dict:
    return jwt.decode(token, secret, algorithms=[ALGO])

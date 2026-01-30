import hashlib

def device_hash(device_id: str, user_agent: str) -> str:
    raw = f"{device_id}|{user_agent}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

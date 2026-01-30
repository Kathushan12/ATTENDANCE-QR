import ipaddress
from fastapi import Request, HTTPException
from app.core.config import settings

def _parse_cidrs():
    parts = [p.strip() for p in settings.WIFI_ALLOWED_CIDRS.split(",") if p.strip()]
    return [ipaddress.ip_network(p) for p in parts]

ALLOWED = _parse_cidrs()

def get_client_ip(request: Request) -> str:
    # If behind proxy (nginx), you may use X-Forwarded-For
    if settings.TRUST_PROXY_HEADERS:
        xff = request.headers.get("x-forwarded-for")
        if xff:
            return xff.split(",")[0].strip()
    return request.client.host

def enforce_wifi_only(request: Request):
    ip_str = get_client_ip(request)
    ip = ipaddress.ip_address(ip_str)
    if not any(ip in net for net in ALLOWED):
        raise HTTPException(status_code=403, detail="Attendance allowed only on University Wi-Fi")

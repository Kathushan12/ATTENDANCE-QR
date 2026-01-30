from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, lecturer, student
from app.core.wifi_guard import get_client_ip  # ✅ add this import

app = FastAPI(title="QR Attendance System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(lecturer.router)
app.include_router(student.router)

@app.get("/health")
def health():
    return {"ok": True}

# ✅ Debug endpoint: check what IP backend sees
@app.get("/debug/ip")
def debug_ip(request: Request):
    return {
        "request_client_host": request.client.host,
        "client_ip_resolved": get_client_ip(request),
        "x_forwarded_for": request.headers.get("x-forwarded-for"),
    }

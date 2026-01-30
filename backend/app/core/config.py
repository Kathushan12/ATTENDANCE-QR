from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    LECTURER_PASSWORD: str
    WIFI_ALLOWED_CIDRS: str = "192.168.0.0/16"
    APP_BASE_URL: str = "http://localhost:5173"
    TRUST_PROXY_HEADERS: bool = True

settings = Settings()

# fastapi_pluggable_auth/config.py
from datetime import timedelta

from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    jwt_secret: str = "CHANGE_ME"
    jwt_algorithm: str = "HS256"
    access_token_expires: timedelta = timedelta(minutes=15)
    refresh_token_expires: timedelta = timedelta(days=7)
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    email_from: str = "no-reply@example.com"
    public_base_url: str = "http://localhost:8000"
    smtp_host: str = "localhost"
    smtp_port: int = 25
    smtp_user: str | None = None
    smtp_password: str | None = None
    verify_token_ttl: timedelta = timedelta(hours=24)
    reset_token_ttl: timedelta = timedelta(hours=1)
    totp_issuer: str = "MyApp"
    single_session: bool = False
    rate_limits: dict[str, str] = {
    "login_ip": "5/minute",
    "login_email": "10/hour",
    "signup_ip": "3/hour",
}


settings = AuthSettings()  # default instance

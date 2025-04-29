# fastapi_pluggable_auth/config.py

from datetime import timedelta
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, AnyHttpUrl
from typing import Literal


class AuthSettings(BaseSettings):
    # Required secrets / connection strings
    jwt_secret: str                             # from JWT_SECRET
    database_url: PostgresDsn                   # from DATABASE_URL
    public_base_url: AnyHttpUrl                 # from PUBLIC_BASE_URL

    # JWT settings
    jwt_algorithm: str = "HS256"
    access_token_expires: timedelta = timedelta(minutes=15)
    refresh_token_expires: timedelta = timedelta(days=7)

    # E-mail / SMTP
    email_provider: Literal["smtp", "sendgrid"] = "smtp"

    email_from: str = "no-reply@example.com"
    smtp_host: str = "localhost"
    smtp_port: int = 25
    smtp_user: str | None = None
    smtp_password: str | None = None

    # SendGrid (or any HTTP-based) settings
    sendgrid_api_key: str | None = None
    sendgrid_from_email: str | None = None

    # E-mail token TTLs
    verify_token_ttl: timedelta = timedelta(hours=24)
    reset_token_ttl: timedelta = timedelta(hours=1)

    # TOTP
    totp_issuer: str = "MyApp"

    # Session behavior
    single_session: bool = False

    # (Optional) rate-limits you might re-enable later
    rate_limits: dict[str, str] = {
        "login_ip": "5/minute",
        "login_email": "10/hour",
        "signup_ip": "3/hour",
    }

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

# instantiate once, shared everywhere
settings = AuthSettings()

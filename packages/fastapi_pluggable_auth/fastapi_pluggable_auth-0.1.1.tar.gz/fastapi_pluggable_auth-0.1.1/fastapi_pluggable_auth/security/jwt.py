# fastapi_pluggable_auth/security/jwt.py
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID
from uuid import uuid4
from jose import JWTError, jwt

from ..config import settings


def _encode(subject: str | UUID, ttl: timedelta, scope: str) -> str:
    data: dict[str, Any] = {
        "sub": str(subject),
        "jti": str(uuid4()),
        "scope": scope,
        "exp": datetime.now(timezone.utc) + ttl,
    }
    return jwt.encode(data, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def create_access_token(user_id: UUID) -> str:
    return _encode(user_id, settings.access_token_expires, "access")


def create_refresh_token(user_id: UUID) -> str:
    return _encode(user_id, settings.refresh_token_expires, "refresh")


def decode_token(token: str, scope_expected: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
        if payload.get("scope") != scope_expected:
            raise JWTError("Wrong token scope")
        return payload
    except JWTError:
        raise

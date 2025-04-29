from datetime import datetime, timedelta, timezone
from jose import jwt
from uuid import UUID
from ..config import settings

_SECRET = settings.jwt_secret
_ALG = settings.jwt_algorithm


def generate_verify_token(user_id: UUID) -> str:
    payload = {
        "sub": str(user_id),
        "scope": "verify",
        "exp": datetime.now(timezone.utc) + settings.verify_token_ttl,
    }
    return jwt.encode(payload, _SECRET, algorithm=_ALG)


def verify_and_get_user_id(token: str) -> UUID:
    from jose import JWTError

    payload = jwt.decode(token, _SECRET, algorithms=[_ALG])
    if payload.get("scope") != "verify":
        raise JWTError("wrong-scope")
    return UUID(payload["sub"])

def generate_reset_token(user_id: UUID) -> str:
    payload = {
        "sub": str(user_id),
        "scope": "reset",
        "exp": datetime.now(timezone.utc) + settings.reset_token_ttl,
    }
    return jwt.encode(payload, _SECRET, algorithm=_ALG)

def verify_reset_token(token: str) -> UUID:
    payload = jwt.decode(token, _SECRET, algorithms=[_ALG])
    if payload.get("scope") != "reset":
        raise JWTError("bad-scope")
    return UUID(payload["sub"])

# fastapi_pluggable_auth/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from .security.jwt import decode_token
from .models import User
from tortoise.exceptions import DoesNotExist

# reusable scheme object
bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
):
    """
    Returns the current authenticated user or raises 401.
    """
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if creds is None:
        raise credentials_error

    token = creds.credentials
    try:
        payload = decode_token(token, "access")
        user_id = payload.get("sub")
        user = await User.get(id=user_id)
    except (JWTError, DoesNotExist):
        raise credentials_error

    return user

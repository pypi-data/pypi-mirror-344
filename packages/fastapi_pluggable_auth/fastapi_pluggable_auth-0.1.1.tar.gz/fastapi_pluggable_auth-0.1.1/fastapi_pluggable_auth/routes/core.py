# fastapi_pluggable_auth/routes/core.py
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Body,
    Depends,
    HTTPException,
    Request,
)
from pydantic import EmailStr
from tortoise.exceptions import IntegrityError

from ..config import settings
from ..dependencies import get_current_user
from ..email.sender import send_email_async
from ..email.tokens import generate_verify_token
from ..models import RefreshToken, User
from ..schemas import LoginData, TokenPair, UserCreate, UserOut
from ..security.hashing import hash_password, verify_password
from ..security.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
)


router = APIRouter(prefix="/auth", tags=["auth"])


# --------------------------------------------------------------------------- signup


@router.post("/signup", response_model=UserOut, status_code=201)
async def signup(data: UserCreate, request: Request, bg: BackgroundTasks):
    """
    Create an account and e-mail a verification link.
    """
    try:
        user = await User.create(
            email=data.email.lower(),
            hashed_password=hash_password(data.password),
        )
    except IntegrityError:
        raise HTTPException(400, "Email already registered")

    token = generate_verify_token(user.id)
    verify_link = f"{settings.public_base_url}/auth/verify/{token}"
    bg.add_task(
        send_email_async,
        user.email,
        "Verify your account",
        "verify.txt.jinja",
        verify_link=verify_link,
    )
    return user


# --------------------------------------------------------------------------- login


@router.post("/login", response_model=TokenPair)
async def login(data: LoginData, request: Request):
    """
    Normal email/password login (+ optional TOTP).
    """
    user = await User.get_or_none(email=data.email.lower())
    if (
        not user
        or not verify_password(data.password, user.hashed_password)
        or not user.is_verified
    ):
        raise HTTPException(401, "Invalid credentials")

    # TOTP enforcement
    if user.totp_secret:
        from ..security.totp import verify_code  # local import avoids cycle

        if not data.code or not verify_code(user.totp_secret, data.code):
            raise HTTPException(401, "Invalid or missing 2-FA code")

    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)
    await RefreshToken.create_for(user.id, refresh, settings.refresh_token_expires)
    return TokenPair(access_token=access, refresh_token=refresh)


# ------------------------------------------------------------------------- refresh
@router.post("/refresh", response_model=TokenPair)
async def refresh(token: str = Body(..., embed=True)):
    """
    Rotate a refresh token → new access & refresh pair.
    """
    payload = decode_token(token, "refresh")
    stored = await RefreshToken.get_or_none(token=token, revoked=False)
    if not stored or stored.expires_at < datetime.now(timezone.utc):
        raise HTTPException(401, "Invalid refresh token")

    user_id = payload["sub"]

    # Revoke the old token *before* issuing new ones (rotation)
    stored.revoked = True
    await stored.save()

    # Optionally kill every other session
    if settings.single_session:
        await RefreshToken.filter(user_id=user_id, revoked=False).update(revoked=True)

    new_refresh = create_refresh_token(user_id)
    await RefreshToken.create_for(user_id, new_refresh, settings.refresh_token_expires)

    return TokenPair(
        access_token=create_access_token(user_id),
        refresh_token=new_refresh,
    )


# ----------------------------------------------------------------------------- me
@router.get("/me", response_model=UserOut)
async def me(current: User = Depends(get_current_user)):
    return current


# -------------------------------------------------------------------------- logout
@router.post("/logout")
async def logout(current: User = Depends(get_current_user)):
    """
    Revoke every active refresh token for the current account.
    """
    await RefreshToken.filter(user_id=current.id, revoked=False).update(revoked=True)
    return {"detail": "Logged out"}

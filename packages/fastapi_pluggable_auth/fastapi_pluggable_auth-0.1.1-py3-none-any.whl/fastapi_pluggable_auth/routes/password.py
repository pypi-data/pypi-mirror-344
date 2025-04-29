# fastapi_pluggable_auth/routes/password.py
from fastapi import APIRouter, BackgroundTasks, Body, HTTPException
from pydantic import EmailStr
from ..models import User, RefreshToken
from jose import JWTError
from ..security.hashing import hash_password
from ..email.tokens import generate_reset_token, verify_reset_token
from ..email.sender import send_email_async
from ..config import settings

router = APIRouter(prefix="/auth", tags=["auth-password"])


@router.post("/forgot-password")
async def forgot_password(email: EmailStr, bg: BackgroundTasks):
    user = await User.get_or_none(email=email.lower())
    if not user:
        return {"detail": "If the account exists, a reset link was sent"}  # silent
    tok = generate_reset_token(user.id)
    link = f"{settings.public_base_url}/auth/reset-password/{tok}"
    bg.add_task(
        send_email_async,
        user.email,
        "Reset your password",
        "reset.txt.jinja",
        reset_link=link,
    )
    return {"detail": "If the account exists, a reset link was sent"}


@router.post("/reset-password/{token}")
async def reset_password(
    token: str, new_password: str = Body(..., embed=True, min_length=8)
):

    try:
        user_id = verify_reset_token(token)
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = hash_password(new_password)
    await user.save()

    # revoke all refresh tokens
    await RefreshToken.filter(user_id=user_id).delete()

    return {"detail": "Password updated"}

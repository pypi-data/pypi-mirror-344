# fastapi_pluggable_auth/routes/email.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from ..email.tokens import generate_verify_token, verify_and_get_user_id
from ..email.sender import send_email_async
from ..models import User

router = APIRouter(prefix="/auth", tags=["auth-email"])

@router.get("/verify/{token}")
async def verify_email(token: str):
    from jose import JWTError
    try:
        user_id = verify_and_get_user_id(token)
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.is_verified:
        return {"detail": "Already verified"}

    user.is_verified = True
    await user.save()
    return {"detail": "Email verified"}

@router.post("/verify/resend")
async def resend_verification(
    email: str, bg: BackgroundTasks
):
    user = await User.get_or_none(email=email.lower())
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.is_verified:
        return {"detail": "Already verified"}

    token = generate_verify_token(user.id)
    link = f"{settings.public_base_url}/auth/verify/{token}"
    bg.add_task(send_email_async, user.email, "Verify your account", "verify.txt.jinja", verify_link=link)
    return {"detail": "Verification e-mail sent"}

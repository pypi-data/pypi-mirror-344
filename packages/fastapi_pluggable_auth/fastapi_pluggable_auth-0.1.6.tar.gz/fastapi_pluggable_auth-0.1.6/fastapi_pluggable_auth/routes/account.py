# fastapi_pluggable_auth/routes/account.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from tortoise.transactions import in_transaction

from ..schemas import UserOut, ProfileUpdate, ChangePassword
from ..models import User, RefreshToken
from ..dependencies import get_current_user
from ..security.hashing import hash_password, verify_password
from ..email.tokens import generate_verify_token
from ..email.sender import send_email_async
from ..config import settings

router = APIRouter(prefix="/account", tags=["account"])


@router.get("", response_model=UserOut)
async def read_profile(current: User = Depends(get_current_user)):
    return current


@router.patch("", response_model=UserOut)
async def update_profile(
    data: ProfileUpdate, bg: BackgroundTasks, current: User = Depends(get_current_user)
):
    if data.email and data.email.lower() != current.email:
        if await User.filter(email=data.email.lower()).exists():
            raise HTTPException(400, "Email already taken")
        current.email = data.email.lower()
        current.is_verified = False
        token = generate_verify_token(current.id)
        link = f"{settings.public_base_url}/auth/verify/{token}"
        bg.add_task(
            send_email_async,
            current.email,
            "Verify new email",
            "verify.txt.jinja",
            verify_link=link,
        )

    if data.display_name is not None:
        current.display_name = data.display_name.strip()

    await current.save()
    return current


@router.post("/change-password", status_code=204)
async def change_password(
    data: ChangePassword, current: User = Depends(get_current_user)
):
    if not verify_password(data.old_password, current.hashed_password):
        raise HTTPException(401, "Old password incorrect")

    current.hashed_password = hash_password(data.new_password)
    await current.save()

    # revoke every refresh token – force re-login everywhere
    await RefreshToken.filter(user_id=current.id, revoked=False).update(revoked=True)
    return


@router.post("/2fa/disable", status_code=204)
async def disable_2fa(current: User = Depends(get_current_user)):
    current.totp_secret = None
    await current.save()
    return


@router.post("/logout-others", status_code=204)
async def logout_others(current: User = Depends(get_current_user)):
    await RefreshToken.filter(user_id=current.id, revoked=False).update(revoked=True)
    return


@router.delete("", status_code=204)
async def delete_account(current: User = Depends(get_current_user)):
    async with in_transaction():
        await RefreshToken.filter(user_id=current.id).delete()
        await current.delete()
    return

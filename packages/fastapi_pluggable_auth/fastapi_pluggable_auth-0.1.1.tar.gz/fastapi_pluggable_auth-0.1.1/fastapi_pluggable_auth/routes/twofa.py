# fastapi_pluggable_auth/routes/twofa.py
from fastapi import APIRouter, Depends, HTTPException
from ..models import User
from ..dependencies import get_current_user
from ..security.totp import (
    generate_totp_secret,
    totp_uri,
    secret_qr_base64,
    verify_code,
)

router = APIRouter(prefix="/auth/2fa", tags=["auth-2fa"])


@router.post("/enable")
async def enable_2fa(current: User = Depends(get_current_user)):
    if current.totp_secret:
        return {"detail": "Already enabled"}
    secret = generate_totp_secret()
    current.totp_secret = secret
    await current.save()
    uri = totp_uri(secret, current.email)
    qr_b64 = secret_qr_base64(uri)
    return {"otpauth_uri": uri, "qr_base64": qr_b64}


@router.post("/verify")
async def verify_2fa(code: str, current: User = Depends(get_current_user)):
    if not current.totp_secret:
        raise HTTPException(status_code=400, detail="2FA not enabled")
    if not verify_code(current.totp_secret, code):
        raise HTTPException(status_code=401, detail="Invalid code")
    return {"detail": "Code accepted"}

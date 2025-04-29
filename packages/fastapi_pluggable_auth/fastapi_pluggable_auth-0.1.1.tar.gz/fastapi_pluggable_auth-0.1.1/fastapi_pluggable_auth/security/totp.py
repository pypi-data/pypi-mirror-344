# fastapi_pluggable_auth/security/totp.py
import pyotp, base64, secrets
from ..config import settings
import qrcode, io, base64

def generate_totp_secret() -> str:
    return pyotp.random_base32()  # 32-char Base32

def totp_uri(secret: str, email: str) -> str:
    return pyotp.totp.TOTP(secret).provisioning_uri(
        name=email,
        issuer_name=settings.totp_issuer,
    )

def verify_code(secret: str, code: str) -> bool:
    return pyotp.TOTP(secret).verify(code, valid_window=1)  # ±30 s leeway

def secret_qr_base64(uri: str) -> str:
    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()
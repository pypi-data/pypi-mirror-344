# fastapi_pluggable_auth/tests/test_totp.py
import pytest, pyotp, httpx
from fastapi_pluggable_auth.models import User
from fastapi_pluggable_auth.schemas import LoginData
GOOD_PW = "TestPass123" 

@pytest.mark.asyncio
async def test_totp_flow(client: httpx.AsyncClient):
    # 1. signup & mark verified
    await client.post("/auth/signup", json={"email": "2@x.com", "password": GOOD_PW})
    u = await User.get(email="2@x.com")
    u.is_verified = True
    await u.save()

    # 2. first login (no 2-FA yet) -> get access token
    r = await client.post("/auth/login", json={"email": "2@x.com", "password": GOOD_PW})
    tok = r.json()["access_token"]
    auth = {"Authorization": f"Bearer {tok}"}

    # 3. enable 2-FA
    r = await client.post("/auth/2fa/enable", headers=auth)
    assert r.status_code == 200
    secret = (await User.get(id=u.id)).totp_secret

    # 4. compute current code
    code = pyotp.TOTP(secret).now()

    # 5. login again, now supplying the code
    r = await client.post(
        "/auth/login",
        json=LoginData(email="2@x.com", password=GOOD_PW, code=code).model_dump(),
    )
    assert r.status_code == 200  # success with 2-FA

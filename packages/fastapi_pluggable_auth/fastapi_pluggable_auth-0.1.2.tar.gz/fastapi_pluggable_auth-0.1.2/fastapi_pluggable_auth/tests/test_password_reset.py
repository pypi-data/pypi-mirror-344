# fastapi_pluggable_auth/tests/test_password_reset.py
import pytest
from fastapi_pluggable_auth.models import User
from fastapi_pluggable_auth.email.tokens import generate_reset_token
GOOD_PW = "TestPass123"
@pytest.mark.asyncio
async def test_password_reset_flow(client):
    # create & verify user
    await client.post("/auth/signup", json={"email":"p@x.com","password":GOOD_PW})
    u = await User.get(email="p@x.com")
    u.is_verified = True
    await u.save()

    # generate token directly (email stubbed)
    tok = generate_reset_token(u.id)

    # reset
    r = await client.post(f"/auth/reset-password/{tok}",
                          json={"new_password":"newpw123"})
    assert r.status_code == 200

    # old login fails
    r = await client.post("/auth/login", json={"email":"p@x.com","password":GOOD_PW})
    assert r.status_code == 401

    # new login works
    r = await client.post("/auth/login", json={"email":"p@x.com","password":"newpw123"})
    assert r.status_code == 200

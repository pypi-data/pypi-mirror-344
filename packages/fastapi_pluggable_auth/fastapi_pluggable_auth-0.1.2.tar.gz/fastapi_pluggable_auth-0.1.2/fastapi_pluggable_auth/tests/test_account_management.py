# fastapi_pluggable_auth/tests/test_account_management.py

import pytest
import httpx
from fastapi_pluggable_auth.models import User

GOOD_PW = "TestPass123"


@pytest.mark.asyncio
async def test_change_password(client: httpx.AsyncClient):
    # 1) Sign up & mark verified
    await client.post(
        "/auth/signup", json={"email": "change@pw.com", "password": GOOD_PW}
    )
    u = await User.get(email="change@pw.com")
    u.is_verified = True
    await u.save()

    # 2) Log in with the old password
    r = await client.post(
        "/auth/login", json={"email": "change@pw.com", "password": GOOD_PW}
    )
    assert r.status_code == 200
    tokens = r.json()
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}

    # 3) Change the password
    r = await client.post(
        "/account/change-password",
        headers=headers,
        json={"old_password": GOOD_PW, "new_password": "newpw123"},
    )
    assert r.status_code == 204, r.text

    # 4) Old refresh & access tokens should be invalid now (optionally test logout behavior)
    #    (depends on whether you revoke tokens on password change)

    # 5) Logging in with the old password should now fail
    r = await client.post(
        "/auth/login", json={"email": "change@pw.com", "password": GOOD_PW}
    )
    assert r.status_code == 401

    # 6) Logging in with the new password should succeed
    r = await client.post(
        "/auth/login", json={"email": "change@pw.com", "password": "newpw123"}
    )
    assert r.status_code == 200

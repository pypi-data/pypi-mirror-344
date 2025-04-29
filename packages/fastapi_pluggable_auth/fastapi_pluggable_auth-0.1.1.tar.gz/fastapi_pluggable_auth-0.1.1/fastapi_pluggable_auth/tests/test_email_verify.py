# fastapi_pluggable_auth/tests/test_email_verify.py
import pytest
from fastapi_pluggable_auth.models import User
from fastapi_pluggable_auth.email.tokens import generate_verify_token

GOOD_PW = "TestPass123"


@pytest.mark.asyncio
async def test_verify_flow(client):
    # 1 signup → sends BG email (ignored in test)
    await client.post("/auth/signup", json={"email": "v@x.com", "password": GOOD_PW})
    # 2 simulate clicking the link
    user = await User.get(email="v@x.com")
    token = generate_verify_token(user.id)
    r = await client.get(f"/auth/verify/{token}")
    assert r.status_code == 200
    # 3 login now succeeds
    r = await client.post("/auth/login", json={"email": "v@x.com", "password": GOOD_PW})
    assert r.status_code == 200

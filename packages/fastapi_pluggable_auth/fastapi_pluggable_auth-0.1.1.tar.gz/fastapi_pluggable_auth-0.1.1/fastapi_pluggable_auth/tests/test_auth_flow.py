# fastapi_pluggable_auth/tests/test_auth_flow.py
import pytest, httpx
from httpx import ASGITransport
from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from fastapi_pluggable_auth.models import User

from fastapi_pluggable_auth import include_auth

GOOD_PW = "TestPass123"

DB_URL = "sqlite://:memory:"
MODELS = {"models": ["fastapi_pluggable_auth.models"]}


@pytest.fixture
async def client():
    # ---- FastAPI app with auth router ----
    app = FastAPI()
    include_auth(app)
    register_tortoise(app, db_url=DB_URL, modules=MODELS, generate_schemas=True)

    # ---- Manually init DB because ASGITransport skips startup handlers ----
    await Tortoise.init(db_url=DB_URL, modules=MODELS)
    await Tortoise.generate_schemas()

    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

    await Tortoise.close_connections()


@pytest.mark.asyncio
async def test_signup_login_refresh(client: httpx.AsyncClient):
    # ------- signup -------
    resp = await client.post(
        "/auth/signup", json={"email": "foo@example.com", "password": GOOD_PW}
    )
    assert resp.status_code == 201, resp.json()

    # ------- flip to verified (DB shortcut) -------
    user = await User.get(email="foo@example.com")
    user.is_verified = True
    await user.save()

    # ------- login -------
    resp = await client.post(
        "/auth/login", json={"email": "foo@example.com", "password": GOOD_PW}
    )
    assert resp.status_code == 200
    tokens = resp.json()

    # ------- me -------
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    resp = await client.get("/auth/me", headers=headers)
    assert resp.status_code == 200

    # ------- refresh -------
    resp = await client.post("/auth/refresh", json={"token": tokens["refresh_token"]})
    assert resp.status_code == 200

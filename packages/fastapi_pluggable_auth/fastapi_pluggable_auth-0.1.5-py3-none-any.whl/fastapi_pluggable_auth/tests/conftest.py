# fastapi_pluggable_auth/tests/conftest.py
import os

os.environ.setdefault("JWT_SECRET", "supersecret")
os.environ.setdefault("DATABASE_URL", "postgres://user:pass@localhost:5432/auth_db")
os.environ.setdefault("PUBLIC_BASE_URL", "http://localhost:8000")
import pytest

from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
import httpx
from tortoise import Tortoise
from fastapi_pluggable_auth import include_auth

DB_URL = "sqlite://:memory:"
MODELS = {"models": ["fastapi_pluggable_auth.models"]}
GOOD_PW = "TestPass123"


@pytest.fixture
def GOOD_PW():
    """Provide a valid password for tests."""
    return "TestPass123"


@pytest.fixture
def WRONG_PW():
    """Provide an invalid password for tests."""
    return "WrongPass99"


@pytest.fixture(scope="function")
async def client():
    """
    Create an in-process FastAPI app with an in-memory SQLite database and return an httpx.AsyncClient.
    """
    app = FastAPI()
    include_auth(app)

    # Initialize Tortoise ORM
    await Tortoise.init(
        db_url=DB_URL,
        modules=MODELS,
    )
    await Tortoise.generate_schemas()

    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client

    # Cleanup
    await Tortoise.close_connections()


@pytest.fixture(autouse=True)
def no_email(monkeypatch):
    """
    Stub async email sending functions to prevent tests from attempting SMTP connections.
    """

    async def _noop(*args, **kwargs):
        return None

    monkeypatch.setattr(
        "fastapi_pluggable_auth.email.sender.send_email_async",
        _noop,
        raising=True,
    )
    monkeypatch.setattr(
        "fastapi_pluggable_auth.routes.core.send_email_async",
        _noop,
        raising=False,
    )
    monkeypatch.setattr(
        "fastapi_pluggable_auth.routes.email.send_email_async",
        _noop,
        raising=False,
    )


@pytest.fixture(autouse=True)
def patch_limiter(monkeypatch):
    """
    No-op fixture since rate limiting is removed.
    """
    pass

# fastapi_pluggable_auth/__init__.py

from fastapi import FastAPI
from .config import AuthSettings, settings as _settings


# Routers -----------------------------------------------------------------
from .routes.core import router as _auth_router
from .routes.email import router as _email_router
from .routes.password import router as _pwd_router
from .routes.twofa import router as _twofa_router
from .routes.account import router as _account_router

_ALL_ROUTERS = (
    _auth_router,
    _email_router,
    _pwd_router,
    _twofa_router,
    _account_router,
)


def include_auth(
    app: FastAPI, *, settings_override: AuthSettings | None = None
) -> None:
    """
    Plug the pluggable-auth module into **app**.

    Parameters
    ----------
    app : FastAPI
        Your main application instance.
    settings_override : AuthSettings | None, default **None**
        Pass an `AuthSettings` instance to replace the module-level
        settings object at runtime (useful in tests).
    """
    # 1) Optional settings swap
    if settings_override is not None:
        global _settings
        _settings = settings_override

    # 5) Register all auth-related routers
    for router in _ALL_ROUTERS:
        app.include_router(router)

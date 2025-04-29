# fastapi_pluggable_auth/schemas.py
from uuid import UUID

from pydantic import BaseModel, EmailStr, constr
from typing import Optional

_PWD = constr(min_length=8, max_length=128)


class UserCreate(BaseModel):
    email: EmailStr
    password: _PWD


class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    is_verified: bool
    display_name: Optional[str] = None


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginData(BaseModel):  # NEW schema just for login
    email: EmailStr
    password: _PWD
    code: str | None = None


class ProfileUpdate(BaseModel):
    email: EmailStr | None = None  # changing triggers new verify token
    display_name: str | None = None


class ChangePassword(BaseModel):
    old_password: str
    new_password: str

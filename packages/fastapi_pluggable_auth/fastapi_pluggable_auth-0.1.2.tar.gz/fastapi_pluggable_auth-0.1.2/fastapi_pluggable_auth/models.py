# fastapi_pluggable_auth/models.py
from datetime import datetime, timezone, timedelta
import uuid

from tortoise import fields, models


class User(models.Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)
    email = fields.CharField(255, unique=True)
    hashed_password = fields.CharField(128)
    is_active = fields.BooleanField(default=True)
    is_verified = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    totp_secret = fields.CharField(32, null=True)
    display_name = fields.CharField(64, null=True)


class RefreshToken(models.Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)
    user = fields.ForeignKeyField("models.User", related_name="refresh_tokens")
    token = fields.CharField(512, unique=True)
    expires_at = fields.DatetimeField()
    created_at = fields.DatetimeField(auto_now_add=True)
    revoked = fields.BooleanField(default=False)  # NEW
    jti = fields.CharField(36, unique=True)  # token ID

    @classmethod
    async def create_for(cls, user_id: uuid.UUID, token: str, ttl: timedelta):
        return await cls.create(
            user_id=user_id,
            token=token,
            jti=str(uuid.uuid4()),
            expires_at=datetime.now(timezone.utc) + ttl,
        )

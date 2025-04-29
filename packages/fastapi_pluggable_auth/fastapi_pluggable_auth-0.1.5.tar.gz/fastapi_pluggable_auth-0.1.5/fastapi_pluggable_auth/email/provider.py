# fastapi_pluggable_auth/email/provider.py

from abc import ABC, abstractmethod
from fastapi_pluggable_auth.config import settings


class EmailProvider(ABC):
    @abstractmethod
    async def send(self, to: str, subject: str, body: str) -> None: ...


class SMTPProvider(EmailProvider):
    async def send(self, to: str, subject: str, body: str):
        import aiosmtplib
        from email.message import EmailMessage

        msg = EmailMessage()
        msg["From"] = settings.email_from
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(body)

        await aiosmtplib.send(
            msg,
            hostname=settings.smtp_host,
            port=settings.smtp_port,
            username=settings.smtp_user,
            password=settings.smtp_password,
        )


class SendGridProvider(EmailProvider):
    async def send(self, to: str, subject: str, body: str):
        import httpx

        payload = {
            "personalizations": [{"to": [{"email": to}]}],
            "from": {"email": settings.sendgrid_from_email},
            "subject": subject,
            "content": [{"type": "text/plain", "value": body}],
        }
        headers = {
            "Authorization": f"Bearer {settings.sendgrid_api_key}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient() as client:
            r = await client.post(
                "https://api.sendgrid.com/v3/mail/send", json=payload, headers=headers
            )
            r.raise_for_status()

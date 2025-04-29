import aiosmtplib
import httpx
import jinja2
from email.message import EmailMessage
from pathlib import Path
from ..config import settings
from .provider import SMTPProvider, SendGridProvider

# Set up Jinja2 environment to load templates
_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(Path(__file__).parent / "templates")
)


def _get_email_provider():
    """
    Factory to return the appropriate email provider based on settings.email_provider
    """
    if settings.email_provider == "sendgrid":
        return SendGridProvider()
    return SMTPProvider()


async def send_email_async(
    to: str,
    subject: str,
    template_name: str,
    **ctx,
):
    # Render the email body from template
    body = _env.get_template(template_name).render(**ctx)

    provider = _get_email_provider()
    await provider.send(to=to, subject=subject, body=body)

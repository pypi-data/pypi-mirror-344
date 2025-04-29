import aiosmtplib, jinja2
from email.message import EmailMessage
from pathlib import Path
from ..config import settings

_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(Path(__file__).parent / "templates")
)


async def send_email_async(to: str, subject: str, template_name: str, **ctx):
    body = _env.get_template(template_name).render(**ctx)

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
        start_tls=True,
    )

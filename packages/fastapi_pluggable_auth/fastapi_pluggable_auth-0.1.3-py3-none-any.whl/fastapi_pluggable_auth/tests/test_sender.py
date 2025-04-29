import pytest
import aiosmtplib
import jinja2
from pathlib import Path
from email.message import EmailMessage

# import the function and the jinja environment object
from fastapi_pluggable_auth.email.sender import send_email_async, _env
from fastapi_pluggable_auth.config import settings


@pytest.mark.asyncio
async def test_send_email_async(monkeypatch, tmp_path):
    # 1) Create a temporary templates folder with one template
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    tmpl = templates_dir / "greet.txt.jinja"
    tmpl.write_text("Hello, {{ name }}!")

    # Monkeypatch the sender's _env to point to our temp templates
    new_env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(templates_dir)))
    monkeypatch.setattr("fastapi_pluggable_auth.email.sender._env", new_env)

    # 2) Stub out aiosmtplib.send to capture its args
    sent = {}

    async def fake_send(
        msg: EmailMessage, hostname, port, username, password, start_tls=True
    ):
        sent["msg"] = msg
        sent["hostname"] = hostname
        sent["port"] = port
        sent["username"] = username
        sent["password"] = password
        sent["start_tls"] = start_tls

    monkeypatch.setattr(aiosmtplib, "send", fake_send)

    # 3) Override settings to known values
    settings.email_from = "from@example.com"
    settings.smtp_host = "smtp.test.com"
    settings.smtp_port = 587
    settings.smtp_user = "user123"
    settings.smtp_password = "pass123"

    # 4) Call the function
    await send_email_async(
        to="to@example.com",
        subject="Test Subject",
        template_name="greet.txt.jinja",
        name="Taylor",
    )

    # 5) Assert SMTP parameters were passed correctly
    assert sent["hostname"] == "smtp.test.com"
    assert sent["port"] == 587
    assert sent["username"] == "user123"
    assert sent["password"] == "pass123"
    assert sent["start_tls"] is True

    # 6) Assert the EmailMessage was constructed correctly
    msg = sent["msg"]
    assert isinstance(msg, EmailMessage)
    assert msg["From"] == "from@example.com"
    assert msg["To"] == "to@example.com"
    assert msg["Subject"] == "Test Subject"
    # get_content() may include a trailing newline, so strip()
    assert msg.get_content().strip() == "Hello, Taylor!"

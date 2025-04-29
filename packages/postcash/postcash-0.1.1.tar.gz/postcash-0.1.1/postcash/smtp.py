# postcash/smtp.py

import smtplib
from email.mime.text import MIMEText
import asyncio
import os

async def send_email(
    to_email: str,
    subject: str,
    body: str,
    from_email: str = None,
    smtp_server: str | None = None,
    smtp_port: int = 587,
    smtp_username: str = None,
    smtp_password: str = None,
):
    """
    Send an email using SMTP.

    Args:
        to_email (str): Recipient email address.
        subject (str): Email subject.
        body (str): Email body (plain text).
        from_email (str, optional): Sender email address. Defaults to None.
        smtp_server (str, optional): SMTP server address. Defaults to environment variable.
        smtp_port (int, optional): SMTP server port. Defaults to environment variable.
        smtp_username (str, optional): SMTP username. Defaults to environment variable.
        smtp_password (str, optional): SMTP password. Defaults to environment variable.
    """
    """Send an email asynchronously using SMTP."""
    # Fallback to environment variables if arguments are missing
    from_email = from_email or os.getenv("POSTCASH_EMAIL_FROM")
    smtp_server = smtp_server or os.getenv("POSTCASH_SMTP_SERVER")
    smtp_port = smtp_port or int(os.getenv("POSTCASH_SMTP_PORT", 587))
    smtp_username = smtp_username or os.getenv("POSTCASH_SMTP_USERNAME")
    smtp_password = smtp_password or os.getenv("POSTCASH_SMTP_PASSWORD")

    if not all([from_email, smtp_server, smtp_username, smtp_password]):
        raise ValueError("SMTP settings are incomplete.")

    def _send():
        msg = MIMEText(body, "plain")
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = to_email

        server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, [to_email], msg.as_string())
        server.quit()

    # Run the blocking SMTP send it in a thread
    await asyncio.to_thread(_send)
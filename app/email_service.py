from pydantic import EmailStr
from .config import smtp_settings
from email.message import EmailMessage
import aiosmtplib

async def generate_email_message(to: EmailStr, subject: str) -> EmailMessage:
    email_message = EmailMessage()
    email_message["From"] = smtp_settings.username
    email_message["To"] = to
    email_message["Subject"] = subject
    return email_message

async def send_email(email_object: EmailMessage) -> None:
    try:
        print("\n===== ПОПЫТКА ОТПРАВКИ EMAIL =====")
        print(f"From: {email_object['From']}")
        print(f"To: {email_object['To']}")
        print(f"Subject: {email_object['Subject']}")
        print(f"SMTP Config: host={smtp_settings.host}, port={smtp_settings.port}, "
              f"use_tls={smtp_settings.use_tls}")
        print("==================================\n")
        await aiosmtplib.send(
            email_object,
            hostname=smtp_settings.host,
            port=smtp_settings.port,
            username=smtp_settings.username,
            password=smtp_settings.password,
            use_tls=smtp_settings.use_tls,
            )
        print("✅ Письмо успешно отправлено")
    except Exception as e:
        print(f"❌ Ошибка при отправке: {e}")
    
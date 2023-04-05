from app.config import settings
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema


async def send_mail(subject: str, recipients: list, body: str):
    message = MessageSchema(subject=subject, recipients=recipients, body=body, subtype="html")
    conf = ConnectionConfig(
        MAIL_USERNAME=settings.mail_username,
        MAIL_PASSWORD=settings.mail_password,
        MAIL_PORT=settings.mail_port,
        MAIL_SERVER=settings.mail_server,
        MAIL_STARTTLS=settings.mail_starttls,
        MAIL_SSL_TLS=settings.mail_ssl_tls,
        MAIL_FROM=settings.mail_from,
        MAIL_FROM_NAME=settings.mail_from_name,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=settings.mail_validate_certs,
    )
    mail = FastMail(conf)
    await mail.send_message(message)

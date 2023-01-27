from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

from app.settings import settings


def get_hashed_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)


def create_reset_password_token(email: str) -> str:
    expires_in = (
        datetime.now(timezone.utc)
        + timedelta(hours=settings.reset_password_token_expire_hours)
    ).timestamp()
    to_encode = {"exp": expires_in, "email": email, "is_active": True}
    return jwt.encode(to_encode, settings.secret_key, settings.algorithm).decode(
        "utf-8"
    )


def verify_reset_password_token(token: str) -> bool:
    token_data = jwt.decode(
        jwt=token, key=settings.secret_key, algorithms=[settings.algorithm]
    )
    print(token_data)
    expires_in = token_data.get("exp")
    is_active = token_data.get("is_active")
    return bool(datetime.now(timezone.utc).timestamp() < expires_in and is_active)


def get_email_from_reset_password_token(token: str) -> str:
    token_data = jwt.decode(
        jwt=token, key=settings.secret_key, algorithms=[settings.algorithm]
    )
    return token_data.get("email")


def html_reset_password_mail(reset_password_token: str):
    return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reset Password</title>
        </head>
        <body>
            <h1>Your token for resetting password</h1>
            <a href="{settings.domain_name}/reset-password/{reset_password_token}">Link</a>
        </body>
        </html>
        """


async def send_mail(subject: str, recipients: list, body: str):
    message = MessageSchema(
        subject=subject, recipients=recipients, body=body, subtype="html"
    )
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
    fm = FastMail(conf)
    await fm.send_message(message)

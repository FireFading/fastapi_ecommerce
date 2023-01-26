from datetime import timedelta
from typing import Optional

from pydantic import BaseSettings


class JWTSettings(BaseSettings):
    authjwt_secret_key: str = "secret"
    authjwt_header_type: Optional[str] = None
    authjwt_header_name: str = "Authorization"
    access_token_expires: timedelta = timedelta(minutes=15)
    refresh_token_expires: timedelta = timedelta(days=30)


class Settings(BaseSettings):
    domain_name: str = ""
    reset_password_token_expire_hours: int = 4
    secret_key: str = "secret"
    algorithm: str = "HS256"

    mail_username: str = "email@yandex.ru"
    mail_password: str = "password"
    mail_port: int = 537
    mail_server: str = "smtp.yandex.ru"
    mail_starttls: bool = True
    mail_ssl_tls: bool = False
    mail_from: str = "email@yandex.ru"
    mail_from_name: str = "mail_from_name"
    mail_validate_certs: bool = False


settings = Settings()

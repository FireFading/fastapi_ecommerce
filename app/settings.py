import os
from datetime import timedelta
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv(dotenv_path="../")


class JWTSettings(BaseSettings):
    authjwt_secret_key: str = os.getenv("AUTHJWT_SECRET_KEY")
    authjwt_header_type: Optional[str] = os.getenv("AUTH_HEADER_TYPE")
    authjwt_header_name: str = os.getenv("AUTHJWT_HEADER_NAME")
    access_token_expires: timedelta = timedelta(
        minutes=os.getenv("ACCESS_TOKEN_EXPIRES")
    )
    refresh_token_expires: timedelta = timedelta(
        days=os.getenv("REFRESH_TOKEN_EXPIRES")
    )


class Settings(BaseSettings):
    domain_name: str = os.getenv("DOMAIN_NAME")

    token_expire_hours: int = os.getenv("TOKEN_EXPIRES_HOURS")
    secret_key: str = os.getenv("SECRET_KEY")
    algorithm: str = os.getenv("ALGORITHM")

    mail_username: str = os.getenv("MAIL_USERNAME")
    mail_password: str = os.getenv("MAIL_PASSWORD")
    mail_port: int = os.getenv("MAIL_PORT")
    mail_server: str = os.getenv("MAIL_SERVER")
    mail_starttls: bool = os.getenv("MAIL_STARTTLS")
    mail_ssl_tls: bool = os.getenv("MAIL_SSL_TLS")
    mail_from: str = os.getenv("MAIL_FROM")
    mail_from_name: str = os.getenv("MAIL_FROM_NAME")
    mail_validate_certs: bool = os.getenv("MAIL_VALIDATE_CERT")


settings = Settings()

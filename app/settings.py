from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv(dotenv_path="../")


class JWTSettings(BaseSettings):
    authjwt_secret_key: str = Field(env="AUTHJWT_SECRET_KEY")
    authjwt_header_type: str | None = Field(env="AUTH_HEADER_TYPE")
    authjwt_header_name: str = Field(env="AUTHJWT_HEADER_NAME")
    access_token_expires: int = Field(env="ACCESS_TOKEN_EXPIRES")
    refresh_token_expires: int = Field(env="REFRESH_TOKEN_EXPIRES")

    class Config:
        env_file = "../.env"


class Settings(BaseSettings):
    domain_name: str = Field(env="DOMAIN_NAME")

    token_expire_hours: int = Field(env="TOKEN_EXPIRES_HOURS")
    secret_key: str = Field(env="SECRET_KEY")
    algorithm: str = Field(env="ALGORITHM")

    mail_username: str = Field(env="MAIL_USERNAME")
    mail_password: str = Field(env="MAIL_PASSWORD")
    mail_port: int = Field(env="MAIL_PORT")
    mail_server: str = Field(env="MAIL_SERVER")
    mail_starttls: bool = Field(env="MAIL_STARTTLS")
    mail_ssl_tls: bool = Field(env="MAIL_SSL_TLS")
    mail_from: str = Field(env="MAIL_FROM")
    mail_from_name: str = Field(env="MAIL_FROM_NAME")
    mail_validate_certs: bool = Field(env="MAIL_VALIDATE_CERT")

    class Config:
        env_file = "../.env"


settings = Settings()

add to .env:

    DOMAIN_NAME=
    TOKEN_EXPIRES_HOURS=

    # password settings
    SECRET_KEY=
    ALGORITHM=

    # jwt settings
    AUTHJWT_SECRET_KEY=
    AUTH_HEADER_TYPE=
    AUTHJWT_HEADER_NAME=
    ACCESS_TOKEN_EXPIRES=
    REFRESH_TOKEN_EXPIRES=

    # mail settings
    MAIL_USERNAME=
    MAIL_PASSWORD=
    MAIL_PORT=
    MAIL_SERVER=
    MAIL_STARTTLS=
    MAIL_SSL_TLS=
    MAIL_FROM=
    MAIL_FROM_NAME=
    MAIL_VALIDATE_CERT=

to run ruff:
    `ruff --show-source --fix ./` in root
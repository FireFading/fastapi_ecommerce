from datetime import timedelta
from typing import Optional

from pydantic import BaseSettings


class JWTSettings(BaseSettings):
    authjwt_secret_key: str = "secret"
    authjwt_header_type: Optional[str] = None
    authjwt_header_name: str = "Authorization"
    access_token_expires: timedelta = timedelta(minutes=15)
    refresh_token_expires: timedelta = timedelta(days=30)

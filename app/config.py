from app.settings import Settings
from dotenv import load_dotenv

load_dotenv(dotenv_path="../")


settings = Settings(_env_file=".env.example")
jwt_settings = Settings(_env_file=".env.example")

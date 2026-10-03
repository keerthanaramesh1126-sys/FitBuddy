from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    google_api_key: str = ""
    gemini_workout_model: str = "gemini-3.8-flash"
    gemini_tip_model: str = "gemini-3.8-flash"
    secret_key: str = "dev_secret_key_replace_in_production_min32chars"
    database_url: str = "sqlite:///./fitbuddy.db"
    admin_username: str = "admin"
    admin_password: str = "changeme"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

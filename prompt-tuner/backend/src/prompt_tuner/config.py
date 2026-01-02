"""Configuration settings for Prompt Tuner."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Server
    host: str = "0.0.0.0"
    port: int = 8002

    # Authentication
    auth_enabled: bool = True
    jwt_secret: str = "prompt-tuner-dev-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440  # 24 hours

    # Admin user
    admin_email: str = "admin@prompttuner.local"
    admin_password: str = "admin"

    # Ingenious API
    ingenious_api_url: str = ""
    ingenious_api_key: str = ""

    model_config = {"env_prefix": "PT_"}


settings = Settings()

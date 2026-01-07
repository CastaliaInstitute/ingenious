"""Configuration for SoCa backend."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment."""

    # Server
    port: int = 8001
    host: str = "0.0.0.0"

    # Authentication
    auth_enabled: bool = True
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24  # 24 hours

    # Admin credentials
    admin_email: str = "admin@soca.local"
    admin_password: str = "admin"

    # Azure Cosmos DB
    cosmos_uri: str = ""
    cosmos_key: str = ""
    cosmos_database: str = "soca"

    # Azure Blob Storage
    storage_connection_string: str = ""
    storage_container: str = "soca-submissions"

    # Prompt Tuner API (hosts AI evaluation via Ingenious)
    ingenious_api_url: str = "http://localhost:8002"
    ingenious_api_key: str = ""

    model_config = {"env_prefix": "SOCA_", "env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()

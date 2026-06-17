# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_db: str = "analytics"
    postgres_user: str = "admin"
    postgres_password: str = "elantra12"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    allowed_origins: list[str] = ["http://localhost:8501", "http://127.0.0.1:8501"]

    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False
    log_level: str = "INFO"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )

    model_config = SettingsConfigDict(env_file=".env", env_parsing_delimiter=",")


settings = Settings()

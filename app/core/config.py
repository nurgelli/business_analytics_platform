# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgres_db: str = "analytics"
    postgres_user: str = "admin"
    postgres_password: str = "elantra12"
    postgres_host: str = "localhost"
    postgres_port: int = 5436

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )

    class Config:
        env_file = ".env"

settings = Settings()
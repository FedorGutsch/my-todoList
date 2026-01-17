from pydantic_settings import BaseSettings
from pydantic import ConfigDict, computed_field, PostgresDsn
from typing import Optional

class Settings(BaseSettings):
    # --- Настройки проекта ---
    PROJECT_NAME: str
    DEBUG: bool = False

    # --- База данных ---
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int

    DATABASE_URL: str  # SQLAlchemy URL

    # --- Порты для Windows (или просто порты) ---
    BACKEND_PORT: int
    CLOUDBEAVER_PORT: int 


    @computed_field
    @property 
    def postgres_link(self) -> PostgresDsn:
        PostgresDsn.build(
            schema = "public", 
            username = self.POSTGRES_USER,
            password = self.POSTGRES_PASSWORD, 
        )

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # игнорировать лишние переменные в .env
    )


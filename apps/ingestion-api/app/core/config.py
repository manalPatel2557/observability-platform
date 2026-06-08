from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parents[4]


class Settings(BaseSettings):
    app_name: str

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        extra="ignore",
    )


settings = Settings()

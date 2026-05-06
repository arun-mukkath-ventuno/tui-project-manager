"""Application configuration."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # Paths
    data_dir: Path = Path("data")
    projects_dir: Path = Path.home() / "Work" / "project-manager" / "task-trackers"

    # Database
    database_url: str = "sqlite:///data/project-manager.db"

    # AI
    openai_api_key: str | None = None
    openai_base_url: str | None = None
    openai_model: str = "gpt-4o-mini"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "RepoPilot AI"
    app_version: str = "0.1.0"
    environment: str = "development"

    github_token: str | None = None
    gemini_api_key: str | None = None

    database_url: str = "sqlite:///./repopilot.db"

    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
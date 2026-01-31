"""Configuration management using Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Railway MCP server configuration."""

    model_config = SettingsConfigDict(
        env_prefix="",
        case_sensitive=False,
    )

    railway_token: str
    railway_api_url: str = "https://backboard.railway.com/graphql/v2"


def get_settings() -> Settings:
    """Get settings instance."""
    return Settings()

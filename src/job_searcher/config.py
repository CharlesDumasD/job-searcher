from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )

    openai_api_key: SecretStr | None = Field(
        default=None,
        alias="OPENAI_API_KEY",
        description="The API key for the OpenAI API",
    )
    openai_model: str = Field(
        default="gpt-4.1-mini",
        description="The OpenAI chat model used by the agent",
    )
    adzuna_app_id: SecretStr | None = Field(
        default=None,
        alias="ADZUNA_APP_ID",
        description="The Adzuna application ID",
    )
    adzuna_app_key: SecretStr | None = Field(
        default=None,
        alias="ADZUNA_APP_KEY",
        description="The Adzuna application key",
    )
    adzuna_country: str = Field(
        default="fr",
        description="The Adzuna country code used for job searches",
    )
    adzuna_results_per_page: int = Field(
        default=10,
        description="The default number of Adzuna results to fetch",
    )
    opik_api_key: SecretStr | None = Field(
        default=None,
        alias="OPIK_API_KEY",
        description="The API key to authenticate with Opik",
    )
    opik_workspace: str | None = Field(
        default=None,
        alias="OPIK_WORKSPACE",
        description=(
            "The Opik workspace name. If not set, the default workspace will be used."
        ),
    )
    opik_project_name: str = Field(
        default="job-searcher",
        alias="OPIK_PROJECT_NAME",
        description="Opik's project name",
    )


def get_settings() -> Settings:
    """Return application settings loaded from the environment."""
    return Settings()

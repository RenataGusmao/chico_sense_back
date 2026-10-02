from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="chicosense-api", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    debug: bool = Field(default=False, alias="DEBUG")
    database_url: str = Field(
        default="postgresql+psycopg://chicosense_user:chicosense_password@localhost:5432/chicosense",
        alias="DATABASE_URL",
    )
    secret_key: str = Field(default="change-this-secret-key", alias="SECRET_KEY")
    thingspeak_base_url: str = Field(default="https://api.thingspeak.com", alias="THINGSPEAK_BASE_URL")
    thingspeak_channel_id: str | None = Field(default=None, alias="THINGSPEAK_CHANNEL_ID")
    thingspeak_read_api_key: str | None = Field(default=None, alias="THINGSPEAK_READ_API_KEY")
    thingspeak_timeout_seconds: float = Field(default=10, alias="THINGSPEAK_TIMEOUT_SECONDS")
    thingspeak_field_mapping_json: str | None = Field(default="{}", alias="THINGSPEAK_FIELD_MAPPING_JSON")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

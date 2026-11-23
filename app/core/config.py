from functools import lru_cache
from urllib.parse import urlsplit

from pydantic import Field, field_validator
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
    access_token_expire_minutes: int = Field(default=30, gt=0, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    cors_allowed_origins: list[str] = Field(default_factory=list, alias="CORS_ALLOWED_ORIGINS")
    thingspeak_base_url: str = Field(default="https://api.thingspeak.com", alias="THINGSPEAK_BASE_URL")
    thingspeak_channel_id: str | None = Field(default=None, alias="THINGSPEAK_CHANNEL_ID")
    thingspeak_read_api_key: str | None = Field(default=None, alias="THINGSPEAK_READ_API_KEY")
    thingspeak_timeout_seconds: float = Field(default=10, alias="THINGSPEAK_TIMEOUT_SECONDS")
    thingspeak_field_mapping_json: str | None = Field(default="{}", alias="THINGSPEAK_FIELD_MAPPING_JSON")

    @field_validator("cors_allowed_origins")
    @classmethod
    def validate_cors_origins(cls, origins: list[str]) -> list[str]:
        validated = []
        for origin in origins:
            origin = origin.strip()
            try:
                parsed = urlsplit(origin)
                port = parsed.port  # Reject malformed ports before application startup.
                valid = (
                    parsed.scheme in ("http", "https")
                    and parsed.hostname
                    and not any(char.isspace() for char in origin)
                    and "*" not in origin and "\\" not in origin
                    and parsed.username is None and parsed.password is None
                    and parsed.path in ("", "/")
                    and not parsed.query and not parsed.fragment
                    and (port is None or port > 0)
                )
            except ValueError:
                valid = False
            if not valid:
                raise ValueError("CORS_ALLOWED_ORIGINS exige origens HTTP(S) explicitas, sem caminhos, credenciais ou curingas.")
            validated.append(origin.rstrip("/"))
        return list(dict.fromkeys(validated))

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

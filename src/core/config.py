import functools
from pathlib import Path

from fastapi_keycloak_middleware import KeycloakConfiguration
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    root_dir: Path = Path(__file__).resolve().parent.parent.parent
    src_dir: Path = root_dir.joinpath("src")

    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000

    ENVIRONMENT: str = "local"
    CORS_ALLOW_ORIGIN_LIST: str = "*"

    CHECK_KEYCLOAK_AUTH: bool = False
    BACKEND_AUTH_URL: str
    KEYCLOAK_URL: str
    KEYCLOAK_REALM: str
    KEYCLOAK_CLIENT_ID: str
    KEYCLOAK_EXCLUDED_ROUTES: list[str] = ["/api/openapi.json", "/api/swagger", "/api/healthcheck"]

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5632
    POSTGRES_USER: str = "web-chat-db"
    POSTGRES_PASSWORD: str = "web-chat-db"
    POSTGRES_DB: str = "web-chat-db"

    @functools.cached_property
    def cors_allow_origins(self) -> list[str]:
        return self.CORS_ALLOW_ORIGIN_LIST.split("&")

    @functools.cached_property
    def keycloak_config(self) -> KeycloakConfiguration:
        return KeycloakConfiguration(
            url=self.KEYCLOAK_URL,
            realm=self.KEYCLOAK_REALM,
            client_id=self.KEYCLOAK_CLIENT_ID,
            reject_on_missing_claim=False,
        )

    @functools.cached_property
    def postgres_host(self) -> str:
        return self.POSTGRES_HOST

    @functools.cached_property
    def postgres_dsn(self) -> str:
        database = self.POSTGRES_DB if self.ENVIRONMENT != "test" else f"{self.POSTGRES_DB}_test"
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.postgres_host}:{self.POSTGRES_PORT}/{database}"
        )


@functools.lru_cache()
def settings():
    return Settings()

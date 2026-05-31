from dataclasses import dataclass
from functools import lru_cache
from os import getenv


@dataclass(frozen=True)
class Settings:
    app_name: str = "FastAPI Practical Template"
    app_version: str = "0.1.0"
    environment: str = "local"
    debug: bool = False


def _get_bool_env(key: str, default: bool = False) -> bool:
    value = getenv(key)

    if value is None:
        return default

    return value.lower() in {"1", "true", "yes", "on"}


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_name=getenv("APP_NAME", Settings.app_name),
        app_version=getenv("APP_VERSION", Settings.app_version),
        environment=getenv("APP_ENV", Settings.environment),
        debug=_get_bool_env("APP_DEBUG", Settings.debug),
    )

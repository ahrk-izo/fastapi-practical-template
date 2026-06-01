from dataclasses import dataclass
from functools import lru_cache
from os import getenv


@dataclass(frozen=True)
class Settings:
    """アプリケーション設定。環境変数から値を読み込み、イミュータブルに保持する。"""

    app_name: str = "FastAPI Practical Template"
    app_version: str = "0.1.0"
    environment: str = "local"
    debug: bool = False
    log_level: str = "INFO"


def _get_bool_env(key: str, default: bool = False) -> bool:
    """環境変数をbool値として取得する。

    "1", "true", "yes", "on"（大文字小文字不問）を True とみなす。
    環境変数が未設定の場合は default を返す。

    Args:
        key: 取得する環境変数名。
        default: 環境変数が未設定の場合に返すデフォルト値。

    Returns:
        変換後のbool値。
    """
    value = getenv(key)

    if value is None:
        return default

    return value.lower() in {"1", "true", "yes", "on"}


@lru_cache
def get_settings() -> Settings:
    """環境変数からSettingsを生成して返す。

    初回呼び出し時に環境変数を読み込み、以降はキャッシュした値を返す。
    テスト時はキャッシュをクリアするために get_settings.cache_clear() を呼ぶこと。

    Returns:
        アプリケーション設定を保持するSettingsインスタンス。
    """
    return Settings(
        app_name=getenv("APP_NAME", Settings.app_name),
        app_version=getenv("APP_VERSION", Settings.app_version),
        environment=getenv("APP_ENV", Settings.environment),
        debug=_get_bool_env("APP_DEBUG", Settings.debug),
        log_level=getenv("LOG_LEVEL", Settings.log_level),
    )

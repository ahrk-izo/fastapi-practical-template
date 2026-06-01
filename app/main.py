import logging

from fastapi import FastAPI

from app.config import get_settings
from app.logging_config import setup_logging

settings = get_settings()
setup_logging(settings.log_level)

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

logger.info(
    "Application started: name=%s version=%s environment=%s debug=%s log_level=%s",
    settings.app_name,
    settings.app_version,
    settings.environment,
    settings.debug,
    settings.log_level,
)


@app.get("/health")
def health_check() -> dict[str, str]:
    """サービスの稼働状態と実行環境名を返す。

    Returns:
        "status": 常に "ok"
        "environment": 環境変数 APP_ENV の値
    """
    logger.debug("Health check requested")

    return {
        "status": "ok",
        "environment": settings.environment,
    }

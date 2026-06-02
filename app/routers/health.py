import logging

from fastapi import APIRouter

from app.config import get_settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    """サービスの稼働状態と実行環境名を返す。

    Returns:
        "status": 常に "ok"
        "environment": 環境変数 APP_ENV の値
    """
    settings = get_settings()
    logger.debug("Health check requested")

    return {
        "status": "ok",
        "environment": settings.environment,
    }

from fastapi import FastAPI

from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)


@app.get("/health")
def health_check() -> dict[str, str]:
    """サービスの稼働状態と実行環境名を返す。

    Returns:
        "status": 常に "ok"
        "environment": 環境変数 APP_ENV の値
    """
    return {
        "status": "ok",
        "environment": settings.environment,
    }

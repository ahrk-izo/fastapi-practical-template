import logging

from fastapi import FastAPI

from app.config import get_settings
from app.logging_config import setup_logging
from app.routers.health import router as health_router

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

app.include_router(health_router)

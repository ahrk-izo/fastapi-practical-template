import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

logger = logging.getLogger(__name__)


def create_error_response(
    *,
    error_type: str,
    message: str,
    status_code: int,
) -> dict[str, Any]:
    """共通エラーレスポンスの辞書を生成する。

    Args:
        error_type: エラーの種別を示す文字列。
        message: エラーの詳細メッセージ。
        status_code: HTTPステータスコード。

    Returns:
        "error" キーにエラー情報を格納した辞書。
    """
    return {
        "error": {
            "type": error_type,
            "message": message,
            "status_code": status_code,
        }
    }


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    """HTTPExceptionを共通エラーレスポンス形式に変換して返す。

    Args:
        request: 発生時のリクエスト情報。
        exc: 発生したHTTPException。

    Returns:
        HTTPステータスコードと共通エラーレスポンスを含むJSONResponse。
    """
    logger.warning(
        "HTTP error occurred: method=%s path=%s status_code=%s detail=%s",
        request.method,
        request.url.path,
        exc.status_code,
        exc.detail,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=create_error_response(
            error_type="http_error",
            message=str(exc.detail),
            status_code=exc.status_code,
        ),
    )


async def unexpected_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """予期しない例外を500エラーとして共通エラーレスポンス形式で返す。

    Args:
        request: 発生時のリクエスト情報。
        exc: 発生した例外。

    Returns:
        500ステータスコードと共通エラーレスポンスを含むJSONResponse。
    """
    logger.exception(
        "Unexpected error occurred: method=%s path=%s",
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content=create_error_response(
            error_type="internal_server_error",
            message="Internal server error",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        ),
    )


def register_exception_handlers(app: FastAPI) -> None:
    """FastAPIアプリケーションに例外ハンドラーを登録する。

    Args:
        app: ハンドラーを登録するFastAPIインスタンス。

    Returns:
        None
    """
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unexpected_exception_handler)

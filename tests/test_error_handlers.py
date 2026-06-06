from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from app.error_handlers import register_exception_handlers


def create_test_client() -> TestClient:
    """例外ハンドラーを登録したテスト用FastAPIクライアントを生成する。

    Returns:
        HTTPエラー・予期しない例外を発生させるエンドポイントを持つTestClient。
    """
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/http-error")
    def raise_http_error() -> None:
        raise HTTPException(status_code=400, detail="Bad request")

    @app.get("/unexpected-error")
    def raise_unexpected_error() -> None:
        raise RuntimeError("Unexpected error")

    return TestClient(app, raise_server_exceptions=False)


def test_http_exception_handler_returns_common_error_response() -> None:
    """HTTPExceptionが発生した場合に共通エラーレスポンス形式で返すことを確認する。

    Returns:
        None
    """
    client = create_test_client()

    response = client.get("/http-error")

    assert response.status_code == 400
    assert response.json() == {
        "error": {
            "type": "http_error",
            "message": "Bad request",
            "status_code": 400,
        }
    }


def test_not_found_returns_common_error_response() -> None:
    """存在しないパスへのリクエストが404の共通エラーレスポンスを返すことを確認する。

    Returns:
        None
    """
    client = create_test_client()

    response = client.get("/not-found")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "type": "http_error",
            "message": "Not Found",
            "status_code": 404,
        }
    }


def test_unexpected_exception_handler_returns_common_error_response() -> None:
    """予期しない例外が発生した場合に500の共通エラーレスポンスを返すことを確認する。

    Returns:
        None
    """
    client = create_test_client()

    response = client.get("/unexpected-error")

    assert response.status_code == 500
    assert response.json() == {
        "error": {
            "type": "internal_server_error",
            "message": "Internal server error",
            "status_code": 500,
        }
    }

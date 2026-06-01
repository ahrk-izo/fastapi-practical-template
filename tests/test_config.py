from app.config import Settings, _get_bool_env, get_settings


def test_get_settings_returns_default_values() -> None:
    """環境変数が未設定の場合にSettingsのデフォルト値が返ることを確認する。

    Returns:
        None
    """
    get_settings.cache_clear()

    settings = get_settings()

    assert settings.app_name == "FastAPI Practical Template"
    assert settings.app_version == "0.1.0"
    assert settings.environment == "local"
    assert settings.debug is False


def test_get_bool_env_returns_default_when_env_not_set(monkeypatch) -> None:
    """環境変数が未設定の場合に_get_bool_envがdefault引数の値を返すことを確認する。

    Args:
        monkeypatch: 環境変数を操作するためのpytestフィクスチャ。

    Returns:
        None
    """
    monkeypatch.delenv("APP_DEBUG", raising=False)

    assert _get_bool_env("APP_DEBUG", default=False) is False
    assert _get_bool_env("APP_DEBUG", default=True) is True


def test_get_bool_env_returns_true_for_truthy_values(monkeypatch) -> None:
    """"true" などのtruthy文字列を設定した場合に_get_bool_envがTrueを返すことを確認する。

    Args:
        monkeypatch: 環境変数を操作するためのpytestフィクスチャ。

    Returns:
        None
    """
    monkeypatch.setenv("APP_DEBUG", "true")

    assert _get_bool_env("APP_DEBUG") is True


def test_get_settings_uses_environment_variables(monkeypatch) -> None:
    """環境変数を設定した場合にget_settingsがその値を反映したSettingsを返すことを確認する。

    Args:
        monkeypatch: 環境変数を操作するためのpytestフィクスチャ。

    Returns:
        None
    """
    monkeypatch.setenv("APP_NAME", "Test API")
    monkeypatch.setenv("APP_VERSION", "9.9.9")
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("APP_DEBUG", "true")

    get_settings.cache_clear()
    settings = get_settings()

    assert settings == Settings(
        app_name="Test API",
        app_version="9.9.9",
        environment="test",
        debug=True,
    )

    get_settings.cache_clear()

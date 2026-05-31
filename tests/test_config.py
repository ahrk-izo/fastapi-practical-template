from app.config import Settings, _get_bool_env, get_settings


def test_get_settings_returns_default_values() -> None:
    get_settings.cache_clear()

    settings = get_settings()

    assert settings.app_name == "FastAPI Practical Template"
    assert settings.app_version == "0.1.0"
    assert settings.environment == "local"
    assert settings.debug is False


def test_get_bool_env_returns_default_when_env_not_set(monkeypatch) -> None:
    monkeypatch.delenv("APP_DEBUG", raising=False)

    assert _get_bool_env("APP_DEBUG", default=False) is False
    assert _get_bool_env("APP_DEBUG", default=True) is True


def test_get_bool_env_returns_true_for_truthy_values(monkeypatch) -> None:
    monkeypatch.setenv("APP_DEBUG", "true")

    assert _get_bool_env("APP_DEBUG") is True


def test_get_settings_uses_environment_variables(monkeypatch) -> None:
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

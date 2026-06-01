import logging

from app.logging_config import setup_logging


def test_setup_logging_sets_log_level() -> None:
    """ログレベルが設定されている場合にsetup_loggingがその値を反映したログレベルを設定することを確認する。

    Returns:
        None
    """
    setup_logging("DEBUG")

    root_logger = logging.getLogger()

    assert root_logger.level == logging.DEBUG

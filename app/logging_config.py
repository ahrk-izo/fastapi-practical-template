import logging


def setup_logging(log_level: str = "INFO") -> None:
    """ロギング設定を初期化する。

    Args:
        log_level: ログレベル。デフォルト: "INFO"。

    Returns:
        None
    """
    logging.basicConfig(
        level=log_level.upper(),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        force=True,
    )

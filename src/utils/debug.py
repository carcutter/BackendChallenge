from flask import current_app


def debug(message: str = "") -> None:
    current_app.logger.debug(message)

"""Logging setup."""

import logging
import sys


def get_logger(name: str) -> logging.Logger:
    """Get a logger with a standard handler.

    Args:
        name: Logger name.

    Returns:
        Configured logger.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

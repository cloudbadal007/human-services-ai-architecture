"""Structured logging with compliance context."""
import logging
import sys

from human_services.utils.config import get_log_level


def get_logger(name: str) -> logging.Logger:
    """Get configured logger with compliance context."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
            )
        )
        logger.addHandler(handler)
        logger.setLevel(getattr(logging, get_log_level().upper(), logging.INFO))
    return logger

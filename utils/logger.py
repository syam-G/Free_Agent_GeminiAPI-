import logging
import sys
from config.settings import settings

def setup_logger(name: str = "AIAgent") -> logging.Logger:
    """Configures structured enterprise console logging."""
    logger = logging.getLogger(name)
    level = getattr(logging, settings.LOG_LEVEL, logging.INFO)
    logger.setLevel(level)

    # Prevent duplicate handlers if re-imported
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-7s | [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

logger = setup_logger()
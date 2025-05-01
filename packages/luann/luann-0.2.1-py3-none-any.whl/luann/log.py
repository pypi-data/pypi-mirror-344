import logging
from pathlib import Path
from sys import stdout
from typing import Optional
from logging.handlers import RotatingFileHandler
from logging.config import dictConfig
from luann.settings import settings

selected_log_level = logging.DEBUG if settings.debug else logging.INFO
def _setup_logfile() -> "Path":
    """ensure the logger filepath is in place
    Returns: the logfile Path
    """
    logfile = Path(settings.luann_dir / "logs" / "luann.log")
    logfile.parent.mkdir(parents=True, exist_ok=True)
    logfile.touch(exist_ok=True)
    return logfile# create rotatating file handler

DEVELOPMENT_LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        # "standard": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
         "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "no_datetime": {
            "format": "%(name)s - %(levelname)s - %(message)s",
        }
    },
    "handlers": {
        "console": {
            "level": selected_log_level,
            "class": "logging.StreamHandler",
            "stream": stdout,
            "formatter": "no_datetime",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": _setup_logfile(),
            "maxBytes": 1024**2 * 10,
            "backupCount": 3,
            "formatter": "standard",
        },
    },
    "loggers": {
        "luann": {
            "level": logging.DEBUG if settings.debug else logging.INFO,
            "handlers": [
                "console",
                "file",
            ],
            "propagate": False,
        },
        "uvicorn": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}
def get_logger(name: Optional[str] = None) -> "logging.Logger":
    """returns the project logger, scoped to a child name if provided
    Args:
        name: will define a child logger
    """
    dictConfig(DEVELOPMENT_LOGGING)
    # logging.config.dictConfig(DEVELOPMENT_LOGGING)
    parent_logger = logging.getLogger("luann")
    if name:
        return parent_logger.getChild(name)
    return parent_logger
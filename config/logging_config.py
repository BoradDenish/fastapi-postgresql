import logging
from logging.config import dictConfig

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": "debug.log",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["file"],
    },
}

def setup_logging():
    dictConfig(LOGGING_CONFIG)
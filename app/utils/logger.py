"""Logging python module."""

import logging
import logging.config
import sys


class StreamFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors."""

    GREY = "\x1b[38;21m"
    GREEN = "\x1b[1;32m"
    YELLOW = "\x1b[33;21m"
    RED = "\x1b[31;21m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"
    MSG_FORMAT = "[%(asctime)s] - [Holocron] - [%(levelname)s] - %(message)s"

    FORMATS = {
        logging.DEBUG: GREY + MSG_FORMAT + RESET,
        logging.INFO: GREEN + MSG_FORMAT + RESET,
        logging.WARNING: YELLOW + MSG_FORMAT + RESET,
        logging.ERROR: RED + MSG_FORMAT + RESET,
        logging.CRITICAL: BOLD_RED + MSG_FORMAT + RESET,
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format the stream output."""
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class LevelHandler(logging.StreamHandler):
    """Custom handler to pick sys.stdout or sys.stderr based on record level."""

    def emit(self, record: logging.LogRecord):
        """Extend logging.StreamHandler to pick stream based on record level."""
        if record.levelno in (logging.ERROR, logging.CRITICAL, logging.WARNING):
            self.stream = sys.stderr
        else:
            self.stream = sys.stdout
        logging.StreamHandler.emit(self, record)


logging_conf = {
    "version": 1,
    "formatters": {
        "stream": {"()": StreamFormatter},
    },
    "handlers": {
        "stream": {
            "()": LevelHandler,
            "level": "INFO",
            "formatter": "stream",
        },
    },
    "loggers": {
        "root": {"level": "INFO", "handlers": ["stream"]},
    },
    "root": {"level": "DEBUG", "handlers": ["stream"]},
    "disable_existing_loggers": False,
}

logging.config.dictConfig(logging_conf)

import logging
import os
from colorama import Fore


INFO = logging.INFO
DEBUG = logging.DEBUG


class NestpyLogger(logging.getLoggerClass()):
    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)

    def info_mapped(self, method, route):
        self.info(f"Mapped {Fore.YELLOW}{method:<6}{Fore.RESET} {route}")


class NestpyFormatter(logging.Formatter):

    FORMATS = {
        logging.DEBUG: Fore.GREEN
        + "[%(name)s]"
        + Fore.RESET
        + " - %(asctime)s - "
        + Fore.CYAN
        + "%(levelname)s - %(message)s"
        + Fore.RESET
        + Fore.RESET,
        logging.INFO: Fore.GREEN
        + "[%(name)s]"
        + Fore.RESET
        + " - %(asctime)s - "
        + Fore.GREEN
        + "%(levelname)s - %(message)s"
        + Fore.RESET,
        logging.WARNING: Fore.GREEN
        + "[%(name)s]"
        + Fore.RESET
        + " - %(asctime)s - "
        + Fore.YELLOW
        + "%(levelname)s - %(message)s"
        + Fore.RESET,
        logging.ERROR: Fore.GREEN
        + "[%(name)s]"
        + Fore.RESET
        + " - %(asctime)s - "
        + Fore.RED
        + "%(levelname)s - %(message)s"
        + Fore.RESET,
        logging.CRITICAL: Fore.MAGENTA
        + "[%(name)s] - %(asctime)s - %(levelname)s - %(message)s"
        + Fore.RESET,
    }

    def format(self, record: logging.LogRecord):
        log_fmt = self.FORMATS.get(record.levelno, self.FORMATS[logging.INFO])
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logging.setLoggerClass(NestpyLogger)


def _configure_logger(name) -> NestpyLogger:
    logger = logging.getLogger(name)
    if not logger.handlers:  # Check if the logger already has handlers
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        logger.setLevel(getattr(logging, log_level, logging.INFO))

        ch = logging.StreamHandler()
        ch.setFormatter(NestpyFormatter())

        logger.addHandler(ch)
        logger.propagate = False
    return logger


nestpy_logger = _configure_logger("nestpy")

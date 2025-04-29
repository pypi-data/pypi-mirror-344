import logging
import sys
from pathlib import Path

from loguru import logger as loguru_logger

from scrapyrta.app.core.config import app_settings
from scrapyrta.app.utils.metaclasses import Singleton

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent


class LoggerConfig(metaclass=Singleton):
    def __init__(self, name: str = "scrapyrta"):
        self.name = name
        self.logger = self._configure_logger()

    def _configure_logger(self):
        # Remove default Loguru handler
        loguru_logger.remove()

        loguru_logger.add(
            sys.stdout,
            level=app_settings.LOG_LEVEL,
            serialize=True,
        )
        loguru_logger.add(
            BASE_DIR / "logs" / f"{self.name}.log",
            level=app_settings.LOG_LEVEL,
            rotation=app_settings.LOG_ROTATION,  # e.g. "10 MB" or "1 day"
            retention=app_settings.LOG_RETENTION,  # e.g. "1 week" or "10 days"
            serialize=True,
        )

        return loguru_logger.bind(name=self.name)

    def get_logger(self):
        return self.logger


def configure_logging():
    class LoguruLogger(logging.Handler):
        def emit(self, record):
            loguru_logger.opt(depth=1).log(record.levelname, record.getMessage())

    logging.getLogger("scrapy").addHandler(LoguruLogger())
    logging.getLogger("scrapy").setLevel(app_settings.LOG_LEVEL)


logger = LoggerConfig().get_logger()

import logging
from pathlib import Path
import warnings
from colab_easy_ui.const import LOG_FILE
warnings.filterwarnings("ignore", message="Duplicate Operation ID")


class CustomFormatter(logging.Formatter):
    def format(self, record):

        # record.module = f"{record.name}:{record.module}".ljust(30)
        record.name = record.name.ljust(10)[:10]
        record.module = record.module.ljust(20)[:20]
        return super().format(record)


class LogSuppressFilter(logging.Filter):
    def filter(self, record):
        return False


class IgnoreConvertRequestFilter(logging.Filter):
    def filter(self, record):
        logfile = f"/{LOG_FILE}" not in record.getMessage()
        return all([logfile])


def setup_logger(logger_name: str, filename: Path, level=logging.DEBUG):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    # custom_datefmt = "%Y-%m-%d %H:%M:%S"
    custom_datefmt = "%H:%M:%S"
    if level == logging.DEBUG:
        # formatter = CustomFormatter("%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s - %(pathname)s - %(lineno)s", datefmt=custom_datefmt)
        formatter = CustomFormatter("%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s - %(pathname)s - %(lineno)s")
    else:
        formatter = CustomFormatter("%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s - %(module)s - %(lineno)s", datefmt=custom_datefmt)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(filename, mode="a", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    for logger_name in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
        logger = logging.getLogger(logger_name)
        logger.propagate = False
        logger.addHandler(file_handler)

    logging.getLogger("uvicorn.access").addFilter(IgnoreConvertRequestFilter())

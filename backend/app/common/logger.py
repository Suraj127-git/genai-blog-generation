import logging
import os
from dotenv import load_dotenv
from typing import Optional

try:
    from logtail import LogtailHandler  # type: ignore
except Exception:
    LogtailHandler = None  # type: ignore

load_dotenv()

def _build_logger(name: Optional[str] = None) -> logging.Logger:
    logger = logging.getLogger(name or __name__)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        formatter = logging.Formatter(
            fmt='%(asctime)s %(levelname)s %(name)s: %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S'
        )
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

        source_token = os.getenv('LOGTAIL_SOURCE_TOKEN')
        host = os.getenv('LOGTAIL_HOST')
        if LogtailHandler and source_token and host:
            handler = LogtailHandler(source_token=source_token, host=host)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
    return logger

logger = _build_logger("blogapp")

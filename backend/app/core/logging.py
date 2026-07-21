import logging
import sys
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
import json
from config import settings

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        if hasattr(record, "request_id"):
            log_entry["request_id"] = record.request_id
        if hasattr(record, "correlation_id"):
            log_entry["correlation_id"] = record.correlation_id
        if record.exc_info and record.exc_info[0]:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(settings.LOG_LEVEL)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)

    # Optional: file logging in production
    # file_handler = RotatingFileHandler("logs/app.log", maxBytes=10_000_000, backupCount=5)
    # file_handler.setFormatter(JsonFormatter())
    # logger.addHandler(file_handler)
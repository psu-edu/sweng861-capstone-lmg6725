import json
import logging
import sys


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(
                record,
                "%Y-%m-%dT%H:%M:%SZ"
            ),
            "level": record.levelname,
            "message": record.getMessage(),
        }

        for field in [
            "request_id",
            "method",
            "path",
            "status_code",
            "event"
        ]:
            if hasattr(record, field):
                log_record[field] = getattr(record, field)

        return json.dumps(log_record)


def configure_logging():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    logger = logging.getLogger("sweng861")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        logger.addHandler(handler)

    logger.propagate = False

    return logger
import logging
from pythonjsonlogger import jsonlogger
from datetime import datetime, timezone


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def __init__(self):
        super().__init__(fmt="%(timestamp)s %(level)s %(correlation_id)s", style='%')

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record['level'] = record.levelname
        log_record['logger'] = record.name
        log_record['timestamp'] = self.formatTime(record)
        if 'correlation_id' not in log_record:
            log_record['correlation_id'] = "N/A"

    def formatTime(self, record, datefmt=None):
        return datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat()


# Setup info logger
info_logger = logging.getLogger("info_logger")
info_handler = logging.FileHandler("requests.log")
info_handler.setFormatter(CustomJsonFormatter())
info_logger.setLevel(logging.INFO)
info_logger.addHandler(info_handler)

# Setup error logger
error_logger = logging.getLogger("error_logger")
error_handler = logging.FileHandler("errors.log")
error_handler.setFormatter(CustomJsonFormatter())
error_logger.setLevel(logging.ERROR)
error_logger.addHandler(error_handler)
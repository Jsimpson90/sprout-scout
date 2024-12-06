import logging
import json
import os
from consts import LOGS_DIR

class JsonFormatter(logging.Formatter):
    """Custom logging formatter to output JSON Lines."""
    def format(self, record):
        location = f"{os.path.abspath(record.pathname)}:{record.lineno}"
        log_record = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "function": record.funcName,
            "message": record.getMessage(),
            "location": location,
            
        }
        return json.dumps(log_record)

def setup_logger():
    # Ensure the logs directory exists
    os.makedirs(LOGS_DIR, exist_ok=True)

    # Create a logger
    logger = logging.getLogger("custom_logger")  # Use a named logger instead of the root logger
    if not logger.hasHandlers():  # Prevent duplicate handlers
        logger.setLevel(logging.DEBUG)  # Set the highest level to capture all logs

        # Create handlers
        debug_handler = logging.FileHandler(os.path.join(LOGS_DIR, "debug.log"), mode='w')
        debug_handler.setLevel(logging.DEBUG)  # Capture all logs
        info_handler = logging.FileHandler(os.path.join(LOGS_DIR, "info.log"), mode='w')
        info_handler.setLevel(logging.INFO)  # Capture only INFO and above logs

        # Set formatters
        json_formatter = JsonFormatter()
        debug_handler.setFormatter(json_formatter)
        info_handler.setFormatter(json_formatter)

        # Add handlers to the logger
        logger.addHandler(debug_handler)
        logger.addHandler(info_handler)

    return logger



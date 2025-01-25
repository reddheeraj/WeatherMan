import logging
import os

# Ensure logs directory exists
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configure logging
LOG_FILE = os.path.join(LOG_DIR, "app.log")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()  # Logs to console
    ]
)

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.

    :param name: Name of the logger (usually the module name).
    :return: Configured logger.
    """
    return logging.getLogger(name)

import logging
from datetime import datetime

# Configure default logging
def setup_logger(name: str, log_file: str, level: int = logging.INFO) -> logging.Logger:
    """
    Sets up a logger with the specified name and log file.

    Args:
        name (str): Name of the logger.
        log_file (str): Path to the log file.
        level (int): Logging level. Default is logging.INFO.

    Returns:
        logging.Logger: Configured logger instance.
    """
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# Utility for formatting dates
def format_date(date: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Formats a datetime object into a string.

    Args:
        date (datetime): The datetime object to format.
        format_str (str): The format string. Default is "%Y-%m-%d %H:%M:%S".

    Returns:
        str: Formatted date string.
    """
    return date.strftime(format_str)

# Example usage
# Example logger setup

logger = setup_logger('core_utils', 'logs/core_utils.log')

if __name__ == "__main__":
    logger.info("Utils module initialized.")
    now = datetime.now()
    formatted_date = format_date(now)
    logger.info(f"Current date formatted: {formatted_date}")
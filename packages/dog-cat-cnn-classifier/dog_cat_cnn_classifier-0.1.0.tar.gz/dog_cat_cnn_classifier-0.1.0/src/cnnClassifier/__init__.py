import yaml 
config = yaml.safe_load(open("config/credentials.yaml")) 
__version__ = config["__version__"]

print("\033[95m" + "Welcome to cnnClassifier version: ", __version__ , " by ", config["username"] + "\033[0m") # ANSI escape code used to add colors or styles to your text in the terminal

import os
import sys
import logging
from colorlog import ColoredFormatter

def get_logger(name: str = "cnnClassifierLogger", log_dir: str = "logs", log_filename: str = "running_logs.log") -> logging.Logger:
    """
    Create and return a logger with both file and colored console handlers.

    Args:
        name (str): Name of the logger.
        log_dir (str): Directory to save log files.
        log_filename (str): Name of the log file.

    Returns:
        logging.Logger: Configured logger.
    """

    # === FORMAT STRINGS ===
    file_log_format = "[%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s]"
    color_log_format = (
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s"
    )

    # === LOG FILE SETUP ===
    os.makedirs(log_dir, exist_ok=True)
    log_filepath = os.path.join(log_dir, log_filename)

    # === FORMATTERS ===
    color_formatter = ColoredFormatter(
        color_log_format,
        datefmt=None,
        reset=True,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )
    file_formatter = logging.Formatter(file_log_format)

    # === HANDLERS ===
    file_handler = logging.FileHandler(filename=log_filepath)
    file_handler.setFormatter(file_formatter)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(color_formatter)

    # === LOGGER SETUP ===
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Avoid adding duplicate handlers
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        logger.propagate = False

    return logger
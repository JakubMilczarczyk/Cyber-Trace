"""
This module delivers the logging logic for the notebooks.
Ensures consistent log formatting across the pipeline.
"""

import logging
import sys

def get_logger(name: str) -> logging.Logger:
    """
    Creates a configured logger instance for Databricks notebooks.
    Format: YYYY-MM-DD HH:MM:SS - Level - Message
    """

    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if cell is re-run
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        # Fix: Changed time format to HH:MM:SS for better readability
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

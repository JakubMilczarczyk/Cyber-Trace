import logging
from src.logger import get_logger

def test_logger_creation():
    """
    Scenario: Create a logger instance.
    Goal: Verify name and level assignment.
    """
    log_name = "TestLogger"
    logger = get_logger(log_name)
    
    assert logger.name == log_name
    assert logger.level == logging.INFO
    assert len(logger.handlers) > 0
    assert isinstance(logger.handlers[0], logging.StreamHandler)

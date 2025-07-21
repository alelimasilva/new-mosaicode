# -*- coding: utf-8 -*-
"""
Tests for the logging system (pure logic, no GUI dependencies).
"""
import logging
import tempfile
import shutil
from pathlib import Path
import pytest

from mosaicode.utils.logger import get_logger

@pytest.fixture
def temp_dir():
    dir_path = Path(tempfile.mkdtemp(prefix="mosaicode_test_"))
    yield dir_path
    if dir_path.exists():
        shutil.rmtree(dir_path)

def test_get_logger():
    logger = get_logger("test_module")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "mosaicode.test_module"

def test_logger_levels():
    logger = get_logger("test_levels")
    # Testa todos os níveis sem levantar exceção
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")
    assert True

def test_logger_properties():
    logger = get_logger("test_properties")
    assert isinstance(logger.name, str)
    assert logger.name == "mosaicode.test_properties"
    assert isinstance(logger.level, int)
    assert isinstance(logger.handlers, list)

def test_multiple_loggers():
    logger1 = get_logger("module1")
    logger2 = get_logger("module2")
    logger3 = get_logger("module1")  # Same name as logger1
    
    # Should be different logger instances
    assert logger1 != logger2
    assert logger2 != logger3
    
    # Same name should return same logger (singleton behavior)
    assert logger1 == logger3

def test_logger_with_formatter():
    logger = get_logger("test_formatter")
    
    # Test that we can set a formatter
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    
    # Add a handler with formatter
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Test logging with formatter
    logger.info("Test message with formatter")
    
    # Should complete without errors
    assert True

def test_logger_level_changes():
    logger = get_logger("test_level_changes")
    
    # Test setting different levels
    logger.setLevel(logging.DEBUG)
    assert logger.level == logging.DEBUG
    
    logger.setLevel(logging.INFO)
    assert logger.level == logging.INFO
    
    logger.setLevel(logging.WARNING)
    assert logger.level == logging.WARNING
    
    logger.setLevel(logging.ERROR)
    assert logger.level == logging.ERROR

def test_logger_handlers():
    logger = get_logger("test_handlers")
    
    # Test adding and removing handlers
    handler = logging.StreamHandler()
    initial_count = len(logger.handlers)
    
    logger.addHandler(handler)
    assert len(logger.handlers) == initial_count + 1
    
    logger.removeHandler(handler)
    assert len(logger.handlers) == initial_count

def test_logger_inheritance():
    parent_logger = get_logger("parent")
    child_logger = get_logger("parent.child")
    
    # Child logger should inherit from parent
    assert child_logger.name.startswith(parent_logger.name)
    
    # Both should be valid loggers
    assert isinstance(parent_logger, logging.Logger)
    assert isinstance(child_logger, logging.Logger)

def test_logger_with_exceptions():
    logger = get_logger("test_exceptions")
    
    # Test logging exceptions
    try:
        raise ValueError("Test exception")
    except ValueError as e:
        logger.exception("Caught exception: %s", str(e))
    
    # Should complete without errors
    assert True

def test_logger_performance():
    logger = get_logger("test_performance")
    
    # Test multiple log messages
    for i in range(100):
        logger.debug(f"Debug message {i}")
        logger.info(f"Info message {i}")
    
    # Should complete without errors
    assert True 
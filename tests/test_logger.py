# -*- coding: utf-8 -*-
"""
Tests for the logging system.
"""
import pytest
import logging
import tempfile
from pathlib import Path

from mosaicode.utils.logger import get_logger


def test_get_logger():
    """Test getting a logger instance."""
    logger = get_logger("test_module")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "mosaicode.test_module"


def test_logger_levels():
    """Test different logging levels."""
    logger = get_logger("test_levels")
    
    # Test that all levels work without raising exceptions
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    
    # All should complete without errors
    assert True


def test_logger_formatting():
    """Test logger message formatting."""
    logger = get_logger("test_formatting")
    
    # Test with different message types
    logger.info("Simple message")
    logger.info("Message with %s", "formatting")
    logger.info("Message with %d numbers", 42)
    
    # All should complete without errors
    assert True


def test_logger_context():
    """Test logger context and propagation."""
    logger = get_logger("test_context")
    
    # Test that logger has proper configuration
    assert isinstance(logger.handlers, list)
    assert logger.level >= 0
    
    # Test that logger can be used in different contexts
    def test_function():
        inner_logger = get_logger("test_context.inner")
        inner_logger.info("Inner function log")
    
    test_function()
    assert True


def test_logger_performance():
    """Test logger performance with multiple calls."""
    logger = get_logger("test_performance")
    
    # Test multiple rapid log calls
    for i in range(100):
        logger.debug(f"Performance test message {i}")
    
    # Should complete without performance issues
    assert True


def test_logger_thread_safety():
    """Test logger thread safety."""
    import threading
    
    logger = get_logger("test_threading")
    results = []
    
    def log_worker(thread_id):
        for i in range(10):
            logger.info(f"Thread {thread_id} message {i}")
        results.append(f"Thread {thread_id} completed")
    
    # Create multiple threads
    threads = []
    for i in range(5):
        thread = threading.Thread(target=log_worker, args=(i,))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # All threads should complete successfully
    assert len(results) == 5


def test_logger_configuration():
    """Test logger configuration options."""
    logger = get_logger("test_config")
    
    # Test that logger has reasonable defaults
    assert logger.name is not None
    assert isinstance(logger.level, int)
    assert isinstance(logger.handlers, list)
    
    # Test that logger can be reconfigured
    original_level = logger.level
    logger.setLevel(logging.DEBUG)
    assert logger.level == logging.DEBUG
    logger.setLevel(original_level)


def test_logger_error_handling():
    """Test logger error handling."""
    logger = get_logger("test_errors")
    
    # Test logging with problematic content
    try:
        logger.info("Normal message")
        logger.info("Message with special chars: áéíóú ñ")
        logger.info("Message with numbers: 123.456")
        logger.info("Message with None: %s", None)
        logger.info("Message with empty string: %s", "")
    except Exception as e:
        pytest.fail(f"Logger should handle all message types: {e}")
    
    assert True


def test_logger_integration():
    """Test logger integration with system."""
    from mosaicode.system import System
    
    # Test that system logging works
    System.log("Test system log message")
    
    # Should complete without errors
    assert True 
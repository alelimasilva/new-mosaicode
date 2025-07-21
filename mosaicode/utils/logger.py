# -*- coding: utf-8 -*-
"""
This module contains the logging configuration for Mosaicode.
"""
import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime


class MosaicodeLogger:
    """
    Centralized logging system for Mosaicode application.
    """
    
    _instance: Optional['MosaicodeLogger'] = None
    _initialized: bool = False
    
    def __new__(cls) -> 'MosaicodeLogger':
        """Singleton pattern for logger."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        """Initialize the logger if not already initialized."""
        if not self._initialized:
            self._setup_logging()
            self._initialized = True
    
    def _setup_logging(self) -> None:
        """Setup logging configuration."""
        # Create logger
        self.logger = logging.getLogger('mosaicode')
        self.logger.setLevel(logging.DEBUG)
        
        # Prevent duplicate handlers
        if self.logger.handlers:
            return
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        simple_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        
        # Console handler (INFO level) - DESABILITADO PARA NÃO MOSTRAR NO TERMINAL
        # console_handler = logging.StreamHandler(sys.stdout)
        # console_handler.setLevel(logging.INFO)
        # console_handler.setFormatter(simple_formatter)
        # self.logger.addHandler(console_handler)
        
        # File handler for all levels
        log_dir = Path.home() / "mosaicode" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"mosaicode_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=1024*1024, backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        self.logger.addHandler(file_handler)
        
        # Error file handler
        error_file = log_dir / f"mosaicode_errors_{datetime.now().strftime('%Y%m%d')}.log"
        error_handler = logging.handlers.RotatingFileHandler(
            error_file, maxBytes=1024*1024, backupCount=3
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        self.logger.addHandler(error_handler)
    
    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message."""
        self.logger.debug(message, extra=kwargs)
    
    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message."""
        self.logger.info(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message."""
        self.logger.warning(message, extra=kwargs)
    
    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message."""
        self.logger.error(message, extra=kwargs)
    
    def critical(self, message: str, **kwargs: Any) -> None:
        """Log critical message."""
        self.logger.critical(message, extra=kwargs)
    
    def exception(self, message: str, exc_info: bool = True, **kwargs: Any) -> None:
        """Log exception with traceback."""
        self.logger.exception(message, exc_info=exc_info, extra=kwargs)


# Global logger instance
logger = MosaicodeLogger()


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for a specific module.
    
    Args:
        name: Module name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(f'mosaicode.{name}')


def log_function_call(func):
    """
    Decorator to log function calls.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    def wrapper(*args, **kwargs):
        logger.debug(f"Calling {func.__name__}", 
                    function=func.__name__,
                    module=func.__module__,
                    args=args,
                    kwargs=kwargs)
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Function {func.__name__} completed successfully",
                        function=func.__name__,
                        result_type=type(result).__name__)
            return result
        except Exception as e:
            logger.exception(f"Function {func.__name__} failed",
                           function=func.__name__,
                           exception=str(e))
            raise
    return wrapper


def log_error_context(context: Dict[str, Any]) -> None:
    """
    Log error context information.
    
    Args:
        context: Context information to log
    """
    logger.error("Error context", **context) 
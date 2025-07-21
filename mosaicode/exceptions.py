# -*- coding: utf-8 -*-
"""
This module contains custom exceptions for the Mosaicode application.
"""
from typing import Optional, Any


class MosaicodeError(Exception):
    """Base exception for Mosaicode application."""
    
    def __init__(self, message: str, details: Optional[Any] = None) -> None:
        """
        Initialize MosaicodeError.
        
        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__(message)
        self.message = message
        self.details = details


class ConfigurationError(MosaicodeError):
    """Raised when configuration is invalid or missing."""
    
    def __init__(self, message: str, config_file: Optional[str] = None) -> None:
        """
        Initialize ConfigurationError.
        
        Args:
            message: Error message
            config_file: Path to the problematic config file
        """
        super().__init__(message, config_file)
        self.config_file = config_file


class BlockLoadError(MosaicodeError):
    """Raised when a block fails to load."""
    
    def __init__(self, message: str, block_type: Optional[str] = None, file_path: Optional[str] = None) -> None:
        """
        Initialize BlockLoadError.
        
        Args:
            message: Error message
            block_type: Type of block that failed to load
            file_path: Path to the block file
        """
        super().__init__(message, {"block_type": block_type, "file_path": file_path})
        self.block_type = block_type
        self.file_path = file_path


class PortLoadError(MosaicodeError):
    """Raised when a port fails to load."""
    
    def __init__(self, message: str, port_type: Optional[str] = None, file_path: Optional[str] = None) -> None:
        """
        Initialize PortLoadError.
        
        Args:
            message: Error message
            port_type: Type of port that failed to load
            file_path: Path to the port file
        """
        super().__init__(message, {"port_type": port_type, "file_path": file_path})
        self.port_type = port_type
        self.file_path = file_path


class CodeTemplateLoadError(MosaicodeError):
    """Raised when a code template fails to load."""
    
    def __init__(self, message: str, template_type: Optional[str] = None, file_path: Optional[str] = None) -> None:
        """
        Initialize CodeTemplateLoadError.
        
        Args:
            message: Error message
            template_type: Type of template that failed to load
            file_path: Path to the template file
        """
        super().__init__(message, {"template_type": template_type, "file_path": file_path})
        self.template_type = template_type
        self.file_path = file_path


class DiagramLoadError(MosaicodeError):
    """Raised when a diagram fails to load."""
    
    def __init__(self, message: str, file_path: Optional[str] = None) -> None:
        """
        Initialize DiagramLoadError.
        
        Args:
            message: Error message
            file_path: Path to the diagram file
        """
        super().__init__(message, file_path)
        self.file_path = file_path


class ValidationError(MosaicodeError):
    """Raised when data validation fails."""
    
    def __init__(self, message: str, field: Optional[str] = None, value: Optional[Any] = None) -> None:
        """
        Initialize ValidationError.
        
        Args:
            message: Error message
            field: Field that failed validation
            value: Value that failed validation
        """
        super().__init__(message, {"field": field, "value": value})
        self.field = field
        self.value = value


class ConnectionError(MosaicodeError):
    """Raised when a connection between blocks fails."""
    
    def __init__(self, message: str, source_block: Optional[str] = None, target_block: Optional[str] = None) -> None:
        """
        Initialize ConnectionError.
        
        Args:
            message: Error message
            source_block: Source block identifier
            target_block: Target block identifier
        """
        super().__init__(message, {"source_block": source_block, "target_block": target_block})
        self.source_block = source_block
        self.target_block = target_block


class FileOperationError(MosaicodeError):
    """Raised when file operations fail."""
    
    def __init__(self, message: str, file_path: Optional[str] = None, operation: Optional[str] = None) -> None:
        """
        Initialize FileOperationError.
        
        Args:
            message: Error message
            file_path: Path to the file
            operation: Operation that failed (read, write, etc.)
        """
        super().__init__(message, {"file_path": file_path, "operation": operation})
        self.file_path = file_path
        self.operation = operation 
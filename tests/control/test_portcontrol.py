# -*- coding: utf-8 -*-
"""
Tests for PortControl class.
Migrated from unittest/TestBase to pytest.
"""
import pytest
import tempfile
import shutil
from pathlib import Path
import logging
from unittest.mock import Mock, patch, MagicMock

from mosaicode.control.portcontrol import PortControl
from mosaicode.model.port import Port

@pytest.fixture
def temp_dir():
    """Create temporary directory for tests."""
    test_dir = Path(tempfile.mkdtemp(prefix="mosaicode_test_"))
    yield test_dir
    if test_dir.exists():
        shutil.rmtree(test_dir)

@pytest.fixture
def test_port():
    """Create a test port."""
    port = Port()
    port.type = "test_port"
    port.label = "Test Port"
    port.name = "test_port"
    port.language = "python"
    port.color = "#FF0000"
    port.multiple = False
    return port

@pytest.fixture
def port_control():
    """Create a PortControl instance."""
    return PortControl()

def test_port_control_initialization(port_control):
    """Test PortControl initialization."""
    assert port_control is not None

@patch('mosaicode.persistence.portpersistence.PortPersistence.load')
def test_load_port(mock_load):
    """Test loading port from file."""
    # Mock the load method to return True
    mock_load.return_value = True
    
    # Test loading port
    result = PortControl.load("test.xml")
    assert result == True
    mock_load.assert_called_once_with("test.xml")

@patch('mosaicode.persistence.portpersistence.PortPersistence.save')
@patch('mosaicode.system.System.get_user_dir')
def test_add_port(mock_get_user_dir, mock_save, test_port, temp_dir):
    """Test adding a port."""
    # Mock user directory to return Path object
    mock_get_user_dir.return_value = temp_dir
    
    # Mock save method
    mock_save.return_value = True
    
    # Test adding port
    PortControl.add_port(test_port)
    
    # Verify save was called
    mock_save.assert_called_once()
    
    # Verify the correct path was used
    expected_path = temp_dir / "extensions" / "python" / "ports"
    mock_save.assert_called_with(test_port, expected_path)

@patch('mosaicode.system.System.get_ports')
@patch('pathlib.Path.unlink')
def test_delete_port_existing(mock_unlink, mock_get_ports, test_port, temp_dir):
    """Test deleting an existing port."""
    # Mock ports dictionary
    mock_ports = {
        "test_port": test_port
    }
    mock_get_ports.return_value = mock_ports
    
    # Set file path for the port
    test_port.file = str(temp_dir / "test_port.json")
    
    # Test deleting port
    result = PortControl.delete_port("test_port")
    assert result == True
    mock_unlink.assert_called_once()

@patch('mosaicode.system.System.get_ports')
def test_delete_port_not_found(mock_get_ports):
    """Test deleting a non-existent port."""
    # Mock empty ports dictionary
    mock_get_ports.return_value = {}
    
    # Test deleting non-existent port
    result = PortControl.delete_port("non_existent_port")
    assert result == False

@patch('mosaicode.system.System.get_ports')
def test_delete_port_no_file(mock_get_ports, test_port):
    """Test deleting a port without file."""
    # Mock ports dictionary
    mock_ports = {
        "test_port": test_port
    }
    mock_get_ports.return_value = mock_ports
    
    # Set file to None
    test_port.file = None
    
    # Test deleting port without file
    result = PortControl.delete_port("test_port")
    assert result == False

@patch('logging.info')
def test_print_port(mock_logging, test_port):
    """Test printing port information."""
    # Test printing port
    PortControl.print_port(test_port)
    
    # Verify logging calls were made with format strings
    expected_calls = [
        "Port Type: {port.type}",
        "Port Label: {port.label}",
        "Port Name: {port.name}",
        "Port Language: {port.language}",
        "Port File: {port.file}",
        "Port Color: {port.color}",
        "Port Multiple: {port.multiple}",
        "Port Required: {port.required}",
        "Port Max Conn: {port.max_conn}",
        "Port Min Conn: {port.min_conn}",
        "---------------------"
    ]
    
    # Check that all expected log messages were called
    for expected_call in expected_calls:
        mock_logging.assert_any_call(expected_call)

def test_print_port_with_file(test_port):
    """Test printing port with file path."""
    # Set file path
    test_port.file = "/path/to/port.json"
    
    with patch('logging.info') as mock_logging:
        # Test printing port
        PortControl.print_port(test_port)
        
        # Verify file path was logged with format string
        mock_logging.assert_any_call("Port File: {port.file}")

def test_add_port_with_different_language(temp_dir):
    """Test adding port with different language."""
    # Create port with different language
    port = Port()
    port.language = "javascript"
    port.type = "js_port"
    
    with patch('mosaicode.persistence.portpersistence.PortPersistence.save') as mock_save:
        with patch('mosaicode.system.System.get_user_dir') as mock_get_user_dir:
            # Mock user directory to return Path object
            mock_get_user_dir.return_value = temp_dir
            
            # Test adding port
            PortControl.add_port(port)
            
            # Verify the correct path was used for javascript
            expected_path = temp_dir / "extensions" / "javascript" / "ports"
            mock_save.assert_called_with(port, expected_path)

def test_port_control_class_methods():
    """Test that all methods are class methods."""
    # Verify all methods are class methods
    assert hasattr(PortControl.load, '__self__')
    assert hasattr(PortControl.add_port, '__self__')
    assert hasattr(PortControl.delete_port, '__self__')
    assert hasattr(PortControl.print_port, '__self__')

def test_delete_port_with_file_path(test_port, temp_dir):
    """Test deleting port with actual file path."""
    # Create a temporary file
    temp_file = temp_dir / "test_port.json"
    temp_file.write_text('{"test": "data"}')
    
    # Mock ports dictionary
    with patch('mosaicode.system.System.get_ports') as mock_get_ports:
        mock_ports = {
            "test_port": test_port
        }
        mock_get_ports.return_value = mock_ports
        
        # Set file path
        test_port.file = str(temp_file)
        
        # Test deleting port
        result = PortControl.delete_port("test_port")
        assert result == True
        
        # Verify file was deleted
        assert not temp_file.exists()


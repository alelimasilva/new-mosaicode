# -*- coding: utf-8 -*-
"""
Tests for system module.
Migrated from unittest/TestBase to pytest.
"""
import pytest
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

from mosaicode.system import System

@pytest.fixture
def system():
    return System()

@pytest.fixture
def mock_config():
    return {
        "app_name": "mosaicode",
        "version": "1.0.0",
        "zoom_levels": {
            "original": 1,
            "zoom_in": 2,
            "zoom_out": 0.5
        },
        "directories": ["extensions", "images", "code-gen"],
        "file_extensions": {
            "diagram": ".mscd",
            "code_template": ".json",
            "port": ".json"
        },
        "extension_server_url": "https://example.com/extensions/"
    }

def test_system_init():
    """Test System initialization."""
    system = System()
    assert system is not None

def test_system_get_system_info():
    """Test getting system information."""
    # Test system constants
    assert System.APP == "mosaicode"
    assert System.VERSION == "0.0.1"
    assert isinstance(System.DATA_DIR, str)

def test_system_get_preferences():
    """Test getting preferences."""
    prefs = System.get_preferences()
    assert prefs is not None

def test_system_get_user_dir():
    """Test getting user directory."""
    user_dir = System.get_user_dir()
    assert isinstance(user_dir, Path)
    assert user_dir.is_absolute()

def test_system_load_system_config():
    """Test loading system configuration."""
    config = System.load_system_config()
    assert isinstance(config, dict)

def test_system_get_system_value():
    """Test getting system configuration values."""
    # Test with existing key
    app_name = System.get_system_value("app_name", "default")
    assert isinstance(app_name, str)
    
    # Test with non-existing key
    non_existing = System.get_system_value("non_existing_key", "default_value")
    assert non_existing == "default_value"

def test_system_get_blocks():
    """Test getting blocks."""
    blocks = System.get_blocks()
    assert isinstance(blocks, dict)

def test_system_get_code_templates():
    """Test getting code templates."""
    templates = System.get_code_templates()
    assert isinstance(templates, dict)

def test_system_get_ports():
    """Test getting ports."""
    ports = System.get_ports()
    assert isinstance(ports, dict)

def test_system_get_list_of_examples():
    """Test getting list of examples."""
    examples = System.get_list_of_examples()
    assert isinstance(examples, list)

def test_system_get_examples():
    """Test getting examples."""
    examples = System.get_examples()
    assert isinstance(examples, list)

def test_system_reload():
    """Test system reload."""
    # Should not raise any exceptions
    System.reload()

def test_system_log():
    """Test logging functionality."""
    # Should not raise any exceptions
    System.log("Test message")

def test_system_set_log():
    """Test set_log method."""
    # Should not raise any exceptions
    System.set_log(None)

def test_system_replace_wildcards():
    """Test wildcard replacement."""
    from mosaicode.model.diagrammodel import DiagramModel
    diagram = DiagramModel()
    diagram.language = "javascript"
    
    # Use correct wildcard format: %t, %d, %l, %n
    name = "test_%l_%n"
    result = System.replace_wildcards(name, diagram)
    assert isinstance(result, str)
    assert result != name  # Should have replaced wildcards

def test_system_get_dir_name():
    """Test get_dir_name method."""
    from mosaicode.model.diagrammodel import DiagramModel
    diagram = DiagramModel()
    diagram.language = "python"  # Definir language para evitar erro
    dir_name = System.get_dir_name(diagram)
    assert dir_name is not None
    assert isinstance(dir_name, str)
    assert len(dir_name) > 0  # Verificar se o diretório foi criado

def test_system_zoom_constants():
    """Test zoom level constants."""
    assert isinstance(System.ZOOM_ORIGINAL, int)
    assert isinstance(System.ZOOM_IN, int)
    assert isinstance(System.ZOOM_OUT, int)
    # Ordem correta: ZOOM_ORIGINAL < ZOOM_IN < ZOOM_OUT
    assert System.ZOOM_ORIGINAL < System.ZOOM_IN < System.ZOOM_OUT


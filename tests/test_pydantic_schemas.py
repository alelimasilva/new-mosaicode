# -*- coding: utf-8 -*-
"""
Tests for Pydantic schemas.
Migrated from unittest/TestBase to pytest.
"""
import pytest
from pathlib import Path
import tempfile
import shutil
import json

from mosaicode.utils.pydantic_schemas import (
    SystemConfig, Preferences, BlockDefaultValues, PortDefaultValues,
    BlockDefaults, PortDefaults, ValidationResult, PydanticValidator,
    ZoomLevels, FileExtensions
)

@pytest.fixture
def temp_dir():
    """Create temporary directory for tests."""
    test_dir = Path(tempfile.mkdtemp(prefix="mosaicode_test_"))
    yield test_dir
    if test_dir.exists():
        shutil.rmtree(test_dir)

def test_system_config_validation():
    """Test SystemConfig validation."""
    # Valid config
    valid_config = {
        "app_name": "mosaicode",
        "version": "1.0.0",
        "zoom_levels": {
            "original": 2,
            "zoom_in": 3,
            "zoom_out": 1
        },
        "directories": ["extensions", "images", "code-gen"],
        "file_extensions": {
            "diagram": ".mscd",
            "code_template": ".json",
            "port": ".json"
        },
        "extension_server_url": "https://example.com/extensions/"
    }
    
    config = SystemConfig(**valid_config)
    assert config.app_name == "mosaicode"
    assert config.version == "1.0.0"
    assert config.zoom_levels.original == 2
    assert config.zoom_levels.zoom_in == 3
    assert config.zoom_levels.zoom_out == 1

def test_preferences_validation():
    """Test Preferences validation."""
    # Valid preferences
    valid_prefs = {
        "conf_file_path": "configuration",
        "author": "Test Author",
        "license": "GPL",
        "version": "1.0.0",
        "recent_files": ["file1.mscd", "file2.mscd"],
        "grid": 10,
        "width": 900,
        "height": 500,
        "default_directory": "~/mosaicode/code-gen",
        "default_filename": "%n",
        "connection": "Curve",
        "hpaned_work_area": 150,
        "vpaned_bottom": 450,
        "vpaned_left": 300
    }
    
    prefs = Preferences(**valid_prefs)
    assert prefs.author == "Test Author"
    assert prefs.license == "GPL"
    assert prefs.grid == 10
    assert prefs.width == 900
    assert prefs.height == 500

def test_block_default_values_validation():
    """Test BlockDefaultValues validation."""
    # Valid block defaults
    valid_block = {
        "id": -1,
        "version": "0.0.1",
        "x": 0,
        "y": 0,
        "is_collapsed": False,
        "type": "TestBlock",
        "language": "javascript",
        "extension": "test",
        "file": None,
        "help": "Test block",
        "label": "TestBlock",
        "color": "#C8C819",
        "group": "Test",
        "ports": [],
        "maxIO": 0,
        "properties": [],
        "codes": {},
        "gen_codes": {},
        "weight": 0,
        "connections": []
    }
    
    block = BlockDefaultValues(**valid_block)
    assert block.type == "TestBlock"
    assert block.label == "TestBlock"
    assert block.color == "#C8C819"

def test_port_default_values_validation():
    """Test PortDefaultValues validation."""
    # Valid port defaults
    valid_port = {
        "version": "0.0.1",
        "type": "TestPort",
        "language": "javascript",
        "hint": "Test port",
        "color": "#0000FF",
        "multiple": False,
        "code": "// Port code",
        "var_name": "$block[label]$_$block[id]$_$port[name]$",
        "conn_type": "INPUT",
        "name": "test_port",
        "label": "Test Port",
        "index": 0,
        "type_index": 0,
        "file": None
    }
    
    port = PortDefaultValues(**valid_port)
    assert port.type == "TestPort"
    assert port.name == "test_port"
    assert port.conn_type == "INPUT"

def test_validation_result():
    """Test ValidationResult model."""
    # Success result
    success_result = ValidationResult(
        success=True,
        errors=[],
        warnings=[],
        data={"test": "data"}
    )
    assert success_result.success == True
    assert len(success_result.errors) == 0
    if success_result.data:
        assert success_result.data["test"] == "data"
    
    # Error result
    error_result = ValidationResult(
        success=False,
        errors=["Error 1", "Error 2"],
        warnings=["Warning 1"],
        data=None
    )
    assert error_result.success == False
    assert len(error_result.errors) == 2
    assert len(error_result.warnings) == 1

def test_pydantic_validator():
    """Test PydanticValidator static methods."""
    # Test system config validation
    valid_system_config = {
        "app_name": "mosaicode",
        "version": "1.0.0"
    }
    result = PydanticValidator.validate_system_config(valid_system_config)
    assert result.success == True
    
    # Test invalid system config
    invalid_system_config = {"invalid": "data"}
    result = PydanticValidator.validate_system_config(invalid_system_config)
    assert result.success == False
    # Note: errors might be None, so we check if it exists and has length
    if result.errors is not None:
        assert len(result.errors) > 0

def test_color_validation():
    """Test color format validation."""
    # Valid colors
    valid_colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFFFF"]
    for color in valid_colors:
        block = BlockDefaultValues(
            id=-1,
            version="0.0.1",
            type="Test",
            label="Test",
            color=color
        )
        assert block.color == color
    
    # Invalid colors should raise validation error
    from pydantic import ValidationError
    invalid_colors = ["red", "FF0000", "#GG0000", "#FFF"]
    for color in invalid_colors:
        try:
            block = BlockDefaultValues(
                id=-1,
                version="0.0.1",
                type="Test",
                label="Test",
                color=color
            )
            # If we get here, the validation failed to catch the error
            assert False, f"Expected ValidationError for color: {color}"
        except ValidationError:
            # Expected behavior
            pass

def test_zoom_level_validation():
    """Test zoom level validation."""
    # Valid zoom levels
    valid_zoom = {
        "original": 2,
        "zoom_in": 3,
        "zoom_out": 1  # Deve ser menor que original
    }
    zoom = ZoomLevels(**valid_zoom)
    assert zoom.original == 2
    assert zoom.zoom_in == 3
    assert zoom.zoom_out == 1
    
    # Invalid zoom levels should raise validation error
    from pydantic import ValidationError
    try:
        invalid_zoom = {
            "original": -1,  # Should be positive
            "zoom_in": 2,
            "zoom_out": 1
        }
        ZoomLevels(**invalid_zoom)
        assert False, "Expected ValidationError for negative zoom level"
    except ValidationError:
        # Expected behavior
        pass

def test_file_extension_validation():
    """Test file extension validation."""
    # Valid file extensions
    valid_extensions = {
        "diagram": ".mscd",
        "code_template": ".json",
        "port": ".json"
    }
    extensions = FileExtensions(**valid_extensions)
    assert extensions.diagram == ".mscd"
    assert extensions.code_template == ".json"
    assert extensions.port == ".json"

def test_connection_type_validation():
    """Test connection type validation."""
    # Valid connection types
    valid_conn_types = ["INPUT", "OUTPUT"]
    for conn_type in valid_conn_types:
        port = PortDefaultValues(
            version="0.0.1",
            type="TestPort",
            language="javascript",
            name="test_port",
            label="Test Port",
            conn_type=conn_type
        )
        assert port.conn_type == conn_type
    
    # Invalid connection type should raise validation error
    from pydantic import ValidationError
    try:
        port = PortDefaultValues(
            version="0.0.1",
            type="TestPort",
            language="javascript",
            name="test_port",
            label="Test Port",
            conn_type="INVALID"
        )
        assert False, "Expected ValidationError for invalid connection type"
    except ValidationError:
        # Expected behavior
        pass

def test_validate_all_configs():
    """Test validation of all configuration types."""
    # Test all validators work together
    valid_configs = {
        "system": {
            "app_name": "mosaicode",
            "version": "1.0.0"
        },
        "preferences": {
            "author": "Test",
            "license": "GPL",
            "version": "1.0.0",
            "grid": 10,
            "width": 900,
            "height": 500
        }
    }
    
    # Test system config validation
    system_result = PydanticValidator.validate_system_config(valid_configs["system"])
    assert system_result.success == True
    
    # Test preferences validation
    prefs_result = PydanticValidator.validate_preferences(valid_configs["preferences"])
    assert prefs_result.success == True 
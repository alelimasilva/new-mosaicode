# -*- coding: utf-8 -*-
"""
Tests for Pydantic schemas (pure logic, no GUI dependencies).
"""
from pathlib import Path
import tempfile
import shutil
import json
import pytest

from mosaicode.utils.pydantic_schemas import (
    SystemConfig, Preferences, BlockDefaultValues, PortDefaultValues,
    BlockDefaults, PortDefaults, ValidationResult, PydanticValidator,
    ZoomLevels, FileExtensions
)

@pytest.fixture
def temp_dir():
    dir_path = Path(tempfile.mkdtemp(prefix="mosaicode_test_"))
    yield dir_path
    if dir_path.exists():
        shutil.rmtree(dir_path)

def test_system_config_validation():
    # Valid config
    valid_config = {
        "app_name": "mosaicode",
        "version": "1.0.0",
        "zoom_levels": {
            "original": 2,
            "zoom_in": 3,
            "zoom_out": 1
        },
        "file_extensions": {
            "diagram": ".mscd",
            "code_template": ".json",
            "port": ".json"
        }
    }
    
    # Test valid config
    config = SystemConfig(**valid_config)
    assert config.app_name == "mosaicode"
    assert config.version == "1.0.0"
    assert isinstance(config.zoom_levels, ZoomLevels)
    assert isinstance(config.file_extensions, FileExtensions)

def test_preferences_validation():
    # Valid preferences
    valid_preferences = {
        "author": "Test Author",
        "license": "MIT",
        "version": "1.0.0"
    }
    
    # Test valid preferences
    prefs = Preferences(**valid_preferences)
    assert prefs.author == "Test Author"
    assert prefs.license == "MIT"
    assert prefs.version == "1.0.0"

def test_block_default_values_validation():
    # Valid block defaults
    valid_block = {
        "id": 1,
        "version": "0.0.1",
        "type": "Test",
        "label": "Test Block",
        "color": "#FF0000"
    }
    
    # Test valid block
    block = BlockDefaultValues(**valid_block)
    assert block.id == 1
    assert block.version == "0.0.1"
    assert block.type == "Test"
    assert block.label == "Test Block"
    assert block.color == "#FF0000"

def test_port_default_values_validation():
    # Valid port defaults
    valid_port = {
        "version": "0.0.1",
        "type": "Test",
        "label": "Test Port",
        "color": "#00FF00"
    }
    
    # Test valid port
    port = PortDefaultValues(**valid_port)
    assert port.version == "0.0.1"
    assert port.type == "Test"
    assert port.label == "Test Port"
    assert port.color == "#00FF00"

def test_color_validation():
    # Valid colors
    valid_colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFFFF"]
    for color in valid_colors:
        block = BlockDefaultValues(
            id=1,
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
        with pytest.raises(ValidationError):
            BlockDefaultValues(
                id=1,
                version="0.0.1",
                type="Test",
                label="Test",
                color=color
            )

def test_zoom_levels_validation():
    # Valid zoom levels
    valid_zoom = {
        "original": 2,
        "zoom_in": 3,
        "zoom_out": 1
    }
    
    zoom = ZoomLevels(**valid_zoom)
    assert zoom.original == 2
    assert zoom.zoom_in == 3
    assert zoom.zoom_out == 1
    
    # Test validation: zoom_out should be less than original
    with pytest.raises(ValueError):
        ZoomLevels(original=1, zoom_in=2, zoom_out=3)

def test_file_extensions_validation():
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

def test_validation_result():
    # Test ValidationResult
    result = ValidationResult(
        success=True,
        errors=[],
        warnings=[]
    )
    assert result.success is True
    assert len(result.errors) == 0
    assert len(result.warnings) == 0
    
    # Test with errors
    result_with_errors = ValidationResult(
        success=False,
        errors=["Error 1", "Error 2"],
        warnings=["Warning 1"]
    )
    assert result_with_errors.success is False
    assert len(result_with_errors.errors) == 2
    assert len(result_with_errors.warnings) == 1

def test_pydantic_validator():
    # Test PydanticValidator
    validator = PydanticValidator()
    
    # Test validate_system_config
    valid_config = {
        "app_name": "mosaicode",
        "version": "1.0.0",
        "zoom_levels": {
            "original": 2,
            "zoom_in": 3,
            "zoom_out": 1
        },
        "file_extensions": {
            "diagram": ".mscd",
            "code_template": ".json",
            "port": ".json"
        }
    }
    
    result = validator.validate_system_config(valid_config)
    assert isinstance(result, ValidationResult)
    assert result.success is True
    
    # Test validate_preferences
    valid_prefs = {
        "author": "Test Author",
        "license": "MIT",
        "version": "1.0.0"
    }
    
    result = validator.validate_preferences(valid_prefs)
    assert isinstance(result, ValidationResult)
    assert result.success is True

def test_validate_all_configs():
    # Test validate_all_configs
    validator = PydanticValidator()
    
    # Test validate_all_configs (no parameters)
    results = validator.validate_all_configs()
    assert isinstance(results, dict)
    # Check that all expected config types are validated
    expected_configs = ["system", "preferences", "blocks", "ports"]
    for config_type in expected_configs:
        assert config_type in results
        assert isinstance(results[config_type], ValidationResult) 
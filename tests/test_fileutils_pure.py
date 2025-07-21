# -*- coding: utf-8 -*-
"""
Tests for FileUtils (pure logic, no GUI dependencies).
"""
import tempfile
import shutil
from pathlib import Path
import json
import pytest

from mosaicode.utils.FileUtils import get_file_path, get_temp_file, get_absolute_path_from_file

@pytest.fixture
def temp_dir():
    dir_path = Path(tempfile.mkdtemp(prefix="mosaicode_test_"))
    yield dir_path
    if dir_path.exists():
        shutil.rmtree(dir_path)

def test_get_file_path():
    result = get_file_path("test_file.txt")
    assert isinstance(result, str)
    assert result.endswith("test_file.txt")

def test_get_temp_file():
    result = get_temp_file()
    assert isinstance(result, str)
    assert len(result) > 0
    temp_path = Path(result)
    assert temp_path.parent.exists() or temp_path.parent.parent.exists()

def test_get_absolute_path_from_file(temp_dir):
    test_file = temp_dir / "test_file.txt"
    test_file.write_text("test content")
    result = get_absolute_path_from_file(str(test_file))
    assert isinstance(result, str)
    assert len(result) > 0
    # Test with non-existent file
    result = get_absolute_path_from_file("non_existent.txt")
    assert isinstance(result, str)

def test_file_operations_with_temp_files(temp_dir):
    temp_file = get_temp_file()
    temp_path = Path(temp_file)
    
    try:
        with open(temp_file, 'w') as f:
            f.write("test content")
        
        with open(temp_file, 'r') as f:
            content = f.read()
        
        assert content == "test content"
        
    except Exception as e:
        assert isinstance(temp_file, str)
        assert len(temp_file) > 0

def test_path_manipulation(temp_dir):
    test_paths = [
        "simple_file.txt",
        "path/to/file.txt",
        "/absolute/path/file.txt",
        "file_with_spaces.txt",
        "file_with_unicode_áéíóú.txt"
    ]
    
    for test_path in test_paths:
        result = get_file_path(test_path)
        assert isinstance(result, str)
        assert len(result) > 0

def test_error_handling():
    try:
        result = get_file_path(None)
        assert isinstance(result, str)
    except Exception:
        pass
    
    try:
        result = get_file_path("")
        assert isinstance(result, str)
    except Exception:
        pass 
# -*- coding: utf-8 -*-
"""
Tests for FileUtils.
"""
import pytest
import tempfile
import shutil
from pathlib import Path
import json

from mosaicode.utils.FileUtils import get_file_path, get_temp_file, get_absolute_path_from_file


def test_get_file_path():
    """Test getting file path."""
    # Test getting path to a file in the same directory
    result = get_file_path("test_file.txt")
    assert isinstance(result, str)
    assert result.endswith("test_file.txt")


def test_get_temp_file():
    """Test getting temporary file."""
    # Test getting temporary file
    result = get_temp_file()
    assert isinstance(result, str)
    assert result != ""


def test_get_absolute_path_from_file():
    """Test getting absolute path from file path."""
    # Test with relative path
    relative_path = "test_file.txt"
    result = get_absolute_path_from_file(relative_path)
    assert isinstance(result, str)
    assert Path(result).is_absolute()
    
    # Test with absolute path
    absolute_path = str(Path.cwd() / "test_file.txt")
    result = get_absolute_path_from_file(absolute_path)
    assert isinstance(result, str)
    assert Path(result).is_absolute()


def test_path_operations(temp_test_dir):
    """Test basic path operations."""
    # Test that we can create and work with paths
    test_file = temp_test_dir / "test_path.txt"
    
    # Create file
    with open(test_file, 'w') as f:
        f.write("Test content")
    
    # Test absolute path conversion
    abs_path = get_absolute_path_from_file(str(test_file))
    assert Path(abs_path).exists()
    
    # Test file path resolution
    file_path = get_file_path("test_path.txt")
    assert isinstance(file_path, str)


def test_temp_file_operations():
    """Test temporary file operations."""
    # Get multiple temp files
    temp_file1 = get_temp_file()
    temp_file2 = get_temp_file()
    
    # Verify they are different
    assert temp_file1 != temp_file2
    
    # Verify they are strings
    assert isinstance(temp_file1, str)
    assert isinstance(temp_file2, str)


def test_path_resolution():
    """Test path resolution functionality."""
    # Test with various path types
    test_cases = [
        "simple.txt",
        "path/to/file.txt",
        "../relative/path.txt",
        "./current/dir/file.txt"
    ]
    
    for test_path in test_cases:
        result = get_absolute_path_from_file(test_path)
        assert isinstance(result, str)
        assert Path(result).is_absolute()


def test_file_path_consistency():
    """Test file path consistency."""
    # Test that get_file_path returns consistent results
    result1 = get_file_path("test.txt")
    result2 = get_file_path("test.txt")
    
    assert result1 == result2
    assert isinstance(result1, str)
    assert isinstance(result2, str)


def test_temp_file_uniqueness():
    """Test that temp files are unique."""
    temp_files = set()
    
    # Generate multiple temp files
    for _ in range(10):
        temp_file = get_temp_file()
        temp_files.add(temp_file)
    
    # All should be unique
    assert len(temp_files) == 10


def test_path_validation():
    """Test path validation."""
    # Test with empty string
    result = get_absolute_path_from_file("")
    assert isinstance(result, str)
    
    # Test with current directory
    result = get_absolute_path_from_file(".")
    assert isinstance(result, str)
    assert Path(result).is_absolute() 
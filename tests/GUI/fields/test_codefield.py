# -*- coding: utf-8 -*-
"""
Tests for CodeField class.
Migrated from unittest to pytest.
"""
import pytest
from mosaicode.GUI.fields.codefield import CodeField


@pytest.fixture
def field():
    """Create a test code field."""
    return CodeField({"label": "test", "value": "True"}, None)


def test_codefield_initialization():
    """Test CodeField initialization with different parameters."""
    # Test with False value
    field_false = CodeField({"label": "test", "value": "False"}, None)
    
    # Test with True value
    field_true = CodeField({"label": "test", "value": "True"}, None)
    
    # All should be created without errors
    assert field_false is not None
    assert field_true is not None


def test_codefield_value_operations(field):
    """Test CodeField value set and get operations."""
    # Test with "False" value
    value1 = "False"
    field.set_value(value1)
    value2 = field.get_value()
    assert value1 == value2, 'incorrect value'
    
    # Test with "True" value
    value1 = "True"
    field.set_value(value1)
    value2 = field.get_value()
    assert value1 == value2, 'incorrect value'
    
    # Test insert_at_cursor method
    field.insert_at_cursor("Test")


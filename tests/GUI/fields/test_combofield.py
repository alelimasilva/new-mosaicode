# -*- coding: utf-8 -*-
"""
Tests for ComboField class.
Migrated from unittest to pytest.
"""
import pytest
from mosaicode.GUI.fields.combofield import ComboField


@pytest.fixture
def field():
    """Create a test combo field."""
    data = {"label": "Test", "value": "a", "name": "", "values": ["a"]}
    return ComboField(data, None)


def test_combofield_initialization():
    """Test ComboField initialization with different parameters."""
    # Test with data containing values
    data = {"label": "Test", "value": "a", "name": "", "values": ["a"]}
    field_data = ComboField(data, None)
    
    # Test with True value
    field_true = ComboField({"label": "test", "value": True}, None)
    
    # All should be created without errors
    assert field_data is not None
    assert field_true is not None


def test_combofield_value_operations():
    """Test ComboField value set and get operations."""
    data = {"label": "Test", "value": "a", "name": "", "values": ["a"]}
    field = ComboField(data, None)
    
    value1 = "a"
    field.set_value(value1)
    value2 = field.get_value()
    assert value1 == value2, 'incorrect value'

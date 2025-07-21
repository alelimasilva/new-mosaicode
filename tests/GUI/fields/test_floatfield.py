# -*- coding: utf-8 -*-
"""
Tests for FloatField class.
Migrated from unittest to pytest.
"""
import pytest
from mosaicode.GUI.fields.floatfield import FloatField


@pytest.fixture
def field():
    """Create a test float field."""
    return FloatField({"label": "test", "value": 0.5}, None)


def test_floatfield_initialization():
    """Test FloatField initialization with different parameters."""
    # Test with 0.5 value
    field_positive = FloatField({"label": "test", "value": 0.5}, None)
    
    # Test with -1 value
    field_negative = FloatField({"label": "test", "value": -1}, None)
    
    # All should be created without errors
    assert field_positive is not None
    assert field_negative is not None


def test_floatfield_value_operations(field):
    """Test FloatField value set and get operations."""
    # Test with negative value
    value1 = -0.5
    field.set_value(value1)
    value2 = field.get_value()
    assert value1 == value2, 'incorrect value'
    
    # Test with positive value
    value1 = 12
    field.set_value(value1)
    value2 = field.get_value()
    assert value1 == value2, 'incorrect value'


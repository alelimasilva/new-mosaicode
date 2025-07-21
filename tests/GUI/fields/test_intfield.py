# -*- coding: utf-8 -*-
"""
Tests for IntField class.
Migrated from unittest to pytest.
"""
import pytest
from mosaicode.GUI.fields.intfield import IntField


@pytest.fixture
def field():
    """Create a test int field."""
    return IntField({"label": "test", "value": 1}, None)


def test_intfield_initialization():
    """Test IntField initialization with different parameters."""
    # Test with value 1
    field_one = IntField({"label": "test", "value": 1}, None)
    
    # Test with value 0
    field_zero = IntField({"label": "test", "value": 0}, None)
    
    # All should be created without errors
    assert field_one is not None
    assert field_zero is not None


def test_intfield_value_operations(field):
    """Test IntField value set and get operations."""
    # Test with value 0
    value1 = 0
    field.set_value(value1)
    value2 = field.get_value()
    assert value1 == value2, 'incorrect value'
    
    # Test with value 100
    value1 = 100
    field.set_value(value1)
    value2 = field.get_value()
    assert value1 == value2, 'incorrect value'


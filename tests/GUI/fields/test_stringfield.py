# -*- coding: utf-8 -*-
"""
Tests for StringField class.
Migrated from unittest to pytest.
"""
import pytest
from mosaicode.GUI.fields.stringfield import StringField


@pytest.fixture
def field():
    """Create a test string field."""
    return StringField({"label": "test", "value": "True"}, None)


def test_stringfield_initialization():
    """Test StringField initialization with different parameters."""
    # Test with False value
    field_false = StringField({"label": "test", "value": "False"}, None)
    
    # Test with True value
    field_true = StringField({"label": "test", "value": "True"}, None)
    
    # All should be created without errors
    assert field_false is not None
    assert field_true is not None


def test_stringfield_value_operations(field):
    """Test StringField value set and get operations."""
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


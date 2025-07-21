# -*- coding: utf-8 -*-
"""
Tests for CheckField class.
Migrated from unittest to pytest.
"""
import pytest
from mosaicode.GUI.fields.checkfield import CheckField


@pytest.fixture
def field():
    """Create a test check field."""
    return CheckField({"label": "test", "value": "True"}, None)


def test_checkfield_initialization():
    """Test CheckField initialization with different parameters."""
    # Test with False value
    field_false = CheckField({"label": "test", "value": "False"}, None)
    
    # Test with True value
    field_true = CheckField({"label": "test", "value": "True"}, None)
    
    # All should be created without errors
    assert field_false is not None
    assert field_true is not None


def test_checkfield_value_operations(field):
    """Test CheckField value set and get operations."""
    # Test with False value
    value1 = False
    field.set_value(value1)
    value2 = field.get_value()
    assert value1 == value2, 'incorrect value'
    
    # Test with True value
    value1 = True
    field.set_value(value1)
    value2 = field.get_value()
    assert value1 == value2, 'incorrect value'


# -*- coding: utf-8 -*-
"""
Tests for LabelField class.
Migrated from unittest to pytest.
"""
import pytest
from mosaicode.GUI.fields.labelfield import LabelField


@pytest.fixture
def field():
    """Create a test label field."""
    return LabelField({"label": "test"}, None)


def test_labelfield_initialization():
    """Test LabelField initialization with different parameters."""
    # Test with label
    field_label = LabelField({"label": "test"}, None)
    
    # Test with empty dict
    field_empty = LabelField({}, "test_value")
    
    # All should be created without errors
    assert field_label is not None
    assert field_empty is not None


def test_labelfield_value_operations(field):
    """Test LabelField value set and get operations."""
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


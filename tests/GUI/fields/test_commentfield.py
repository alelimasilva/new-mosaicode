# -*- coding: utf-8 -*-
"""
Tests for CommentField class.
Migrated from unittest to pytest.
"""
import pytest
from mosaicode.GUI.fields.commentfield import CommentField


@pytest.fixture
def field():
    """Create a test comment field."""
    return CommentField({"label": "test", "value": "True"}, None)


def test_commentfield_initialization():
    """Test CommentField initialization with different parameters."""
    # Test with False value
    field_false = CommentField({"label": "test", "value": "False"}, None)
    
    # Test with True value
    field_true = CommentField({"label": "test", "value": "True"}, None)
    
    # All should be created without errors
    assert field_false is not None
    assert field_true is not None


def test_commentfield_value_operations(field):
    """Test CommentField value set and get operations."""
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


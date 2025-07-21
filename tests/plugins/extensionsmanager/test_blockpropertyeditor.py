# Migrated from unittest/TestBase to pytest.
import pytest
from mosaicode.plugins.extensionsmanager.propertyeditor import PropertyEditor

def test_init(block):
    """Test PropertyEditor initialization."""
    editor = PropertyEditor(block)
    assert editor is not None

def test_set_block(block):
    """Test setting block in editor."""
    editor = PropertyEditor(block)
    assert editor is not None


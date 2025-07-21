# -*- coding: utf-8 -*-
"""
Tests for BlockCodeEditor class.
Migrated from unittest to pytest.
"""
import pytest
from mosaicode.plugins.extensionsmanager.blockmanager import BlockManager
from mosaicode.plugins.extensionsmanager.blockeditor import BlockEditor
from mosaicode.plugins.extensionsmanager.blockcodeeditor import BlockCodeEditor


@pytest.fixture
def block_code_editor(block):
    """Create a test block code editor."""
    return BlockCodeEditor(block)


def test_blockcodeeditor_initialization(block_code_editor):
    """Test BlockCodeEditor initialization."""
    assert block_code_editor is not None


def test_blockcodeeditor_base(block):
    """Test BlockCodeEditor base functionality."""
    widget = BlockCodeEditor(block)
    
    assert widget is not None


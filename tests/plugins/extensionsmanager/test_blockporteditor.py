# -*- coding: utf-8 -*-
"""
Tests for BlockPortEditor class.
Migrated from unittest to pytest.
"""
import pytest
from mosaicode.plugins.extensionsmanager.blockmanager import BlockManager
from mosaicode.plugins.extensionsmanager.blockeditor import BlockEditor
from mosaicode.plugins.extensionsmanager.blockporteditor import BlockPortEditor


@pytest.fixture
def block_port_editor(block):
    """Create a test block port editor."""
    return BlockPortEditor(block)


def test_blockporteditor_initialization(block_port_editor):
    """Test BlockPortEditor initialization."""
    assert block_port_editor is not None


def test_blockporteditor_base(block):
    """Test BlockPortEditor base functionality."""
    widget = BlockPortEditor(block)
    
    assert widget is not None

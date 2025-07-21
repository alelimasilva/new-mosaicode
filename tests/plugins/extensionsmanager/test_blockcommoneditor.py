# -*- coding: utf-8 -*-
"""
Tests for BlockCommonEditor class.
Migrated from unittest to pytest.
"""
import pytest
from mosaicode.plugins.extensionsmanager.blockmanager import BlockManager
from mosaicode.plugins.extensionsmanager.blockeditor import BlockEditor
from mosaicode.plugins.extensionsmanager.blockcommoneditor import BlockCommonEditor


@pytest.fixture
def block_common_editor(block):
    """Create a test block common editor."""
    return BlockCommonEditor(block)


def test_blockcommoneditor_initialization(block_common_editor):
    """Test BlockCommonEditor initialization."""
    assert block_common_editor is not None


def test_blockcommoneditor_base(block):
    """Test BlockCommonEditor base functionality."""
    widget = BlockCommonEditor(block)
    
    assert widget is not None

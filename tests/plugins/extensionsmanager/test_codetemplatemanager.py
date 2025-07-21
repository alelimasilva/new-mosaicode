# -*- coding: utf-8 -*-
"""
Tests for CodeTemplateManager class.
Migrated from unittest to pytest.
"""
import pytest
from mosaicode.plugins.extensionsmanager.codetemplatemanager import CodeTemplateManager


@pytest.fixture
def code_template_manager(main_window):
    """Create a test code template manager."""
    return CodeTemplateManager(main_window)


def test_codetemplatemanager_initialization(code_template_manager):
    """Test CodeTemplateManager initialization."""
    assert code_template_manager is not None


def test_codetemplatemanager_base(main_window):
    """Test CodeTemplateManager base functionality."""
    widget = CodeTemplateManager(main_window)
    
    assert widget is not None


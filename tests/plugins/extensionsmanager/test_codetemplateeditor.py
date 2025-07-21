# -*- coding: utf-8 -*-
"""
Tests for CodeTemplateEditor class.
Migrated from unittest to pytest.
"""
import pytest
from mosaicode.system import System
from mosaicode.plugins.extensionsmanager.codetemplateeditor import CodeTemplateEditor
from mosaicode.plugins.extensionsmanager.codetemplatemanager import CodeTemplateManager


@pytest.fixture
def code_template_editor(main_window):
    """Create a test code template editor."""
    code_template_manager = CodeTemplateManager(main_window)
    code_template_name = "Test"
    return CodeTemplateEditor(code_template_manager, code_template_name)


def test_codetemplateeditor_initialization(code_template_editor):
    """Test CodeTemplateEditor initialization."""
    assert code_template_editor is not None


def test_codetemplateeditor_base(main_window):
    """Test CodeTemplateEditor base functionality."""
    code_template_manager = CodeTemplateManager(main_window)
    code_template_name = "Test"
    widget = CodeTemplateEditor(code_template_manager, code_template_name)
    
    assert widget is not None


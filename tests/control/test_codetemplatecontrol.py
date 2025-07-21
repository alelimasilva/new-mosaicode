# -*- coding: utf-8 -*-
"""
Tests for CodeTemplateControl class.
Migrated from unittest/TestBase to pytest.
"""
import pytest
import os
from mosaicode.system import System
from mosaicode.control.codetemplatecontrol import CodeTemplateControl

@pytest.fixture
def code_template():
    """Create a test code template."""
    from mosaicode.model.codetemplate import CodeTemplate
    template = CodeTemplate()
    template.name = "Test Template"
    template.language = "python"
    template.command = "python test.py"
    template.description = "Test template description"
    template.codes = {"main": "print('Hello World')"}
    template.code_parts = ["main"]
    template.properties = []
    return template

def test_init():
    """Test CodeTemplateControl initialization."""
    CodeTemplateControl()

def test_load():
    """Test loading code template from file."""
    # Test with non-existent file (should handle gracefully)
    CodeTemplateControl.load("non_existent_file.xml")

def test_add_code_template(code_template):
    """Test adding a code template."""
    System()
    System.reload()
    CodeTemplateControl.add_code_template(code_template)

def test_delete_code_template():
    """Test deleting a code template."""
    # Test with non-existent template
    result = CodeTemplateControl.delete_code_template("non_existent_template")
    assert result == False

def test_print_template(code_template):
    """Test printing template information."""
    CodeTemplateControl.print_template(code_template)

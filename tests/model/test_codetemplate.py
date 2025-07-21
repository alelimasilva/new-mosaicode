# -*- coding: utf-8 -*-
"""
Tests for CodeTemplate class.
Migrated from unittest/TestBase to pytest.
"""
import pytest
from mosaicode.model.codetemplate import CodeTemplate
from mosaicode.model.port import Port

@pytest.fixture
def code_template():
    return CodeTemplate()

def test_codetemplate_init():
    CodeTemplate()

def test_codetemplate_equals():
    code1 = CodeTemplate()
    code2 = CodeTemplate()
    assert code1.equals(code2) == True

    code1.language = "Test"
    assert code1.equals(code2) == False

    code1 = CodeTemplate()
    if code1.__dict__:
        first_key = list(code1.__dict__.keys())[0]
        code1.__dict__.pop(first_key, None)
    assert code2.equals(code1) == False

def test_codetemplate_set_properties():
    code = CodeTemplate()
    code.properties = [{"name": "test", "label": "test", "value": "test", "type": "test"}]

    code.set_properties({"out": "SET"})
    code.set_properties({"test": "SET"})
    assert code.properties[0]["value"] == "SET"

def test_codetemplate_get_properties():
    code = CodeTemplate()
    properties = code.get_properties()
    assert isinstance(properties, list)

def test_codetemplate_str():
    code = CodeTemplate()
    string = code.__str__()
    assert isinstance(string, str)
    assert string == str(code.__class__.__module__)

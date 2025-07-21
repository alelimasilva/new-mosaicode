# Migrated from unittest/TestBase to pytest.
import os
import pytest
from mosaicode.persistence.codetemplatepersistence import CodeTemplatePersistence
from mosaicode.model.codetemplate import CodeTemplate

def test_load_non_existent():
    """Test loading non-existent code template."""
    result = CodeTemplatePersistence.load("/tmp/nonexistent.json")
    assert result is None

def test_load_save(codetemplate):
    """Test load and save code template."""
    result = CodeTemplatePersistence.save(codetemplate, "/tmp/")
    assert result is True
    
    file_name = "/tmp/" + codetemplate.name + ".json"
    loaded_template = CodeTemplatePersistence.load(file_name)
    assert loaded_template is not None
    assert loaded_template.name == codetemplate.name
    assert loaded_template.language == codetemplate.language
    
    if os.path.exists(file_name):
        os.remove(file_name)

def test_load_wrong_file():
    """Test loading file with wrong format."""
    with open("/tmp/wrong.json", "w") as f:
        f.write("not a code template")
    result = CodeTemplatePersistence.load("/tmp/wrong.json")
    assert result is None
    os.remove("/tmp/wrong.json")

def test_save_no_permission(codetemplate):
    """Test saving without permission."""
    result = CodeTemplatePersistence.save(codetemplate, "/root/")
    assert result is False


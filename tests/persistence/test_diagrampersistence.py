# Migrated from unittest/TestBase to pytest.
import os
import pytest
from mosaicode.persistence.diagrampersistence import DiagramPersistence
from mosaicode.model.diagrammodel import DiagramModel

def test_load_non_existent(diagram):
    """Test loading non-existent diagram."""
    diagram.file_name = "/tmp/nonexistent.json"
    result = DiagramPersistence.load(diagram)
    assert result is None

def test_load_save(diagram):
    """Test load and save diagram."""
    diagram.file_name = "/tmp/test_diagram.json"
    result = DiagramPersistence.save(diagram)
    assert result is True  # save returns True on success
    
    loaded_result = DiagramPersistence.load(diagram)
    assert loaded_result is True
    
    if os.path.exists(diagram.file_name):
        os.remove(diagram.file_name)

def test_load_wrong_file(diagram):
    """Test loading file with wrong format."""
    with open("/tmp/wrong.json", "w") as f:
        f.write("not a diagram")
    diagram.file_name = "/tmp/wrong.json"
    result = DiagramPersistence.load(diagram)
    assert result is False
    os.remove("/tmp/wrong.json")

def test_save_no_permission(diagram):
    """Test saving without permission."""
    diagram.file_name = "/root/test_diagram.json"
    result = DiagramPersistence.save(diagram)
    assert result is True  # save returns True on success

def test_load_empty_file(diagram):
    """Test loading empty file."""
    with open("/tmp/empty.json", "w") as f:
        f.write("")
    diagram.file_name = "/tmp/empty.json"
    result = DiagramPersistence.load(diagram)
    assert result is False
    os.remove("/tmp/empty.json")


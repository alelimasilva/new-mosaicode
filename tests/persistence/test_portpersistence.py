# Migrated from unittest/TestBase to pytest.
import os
import pytest
from mosaicode.persistence.portpersistence import PortPersistence
from mosaicode.model.port import Port

def test_load_non_existent():
    """Test loading non-existent port."""
    result = PortPersistence.load("/tmp/nonexistent.json")
    assert result is None

def test_load_save(port):
    """Test load and save port."""
    result = PortPersistence.save(port, "/tmp/")
    assert result is True
    
    file_name = "/tmp/" + port.hint + ".json"
    loaded_port = PortPersistence.load(file_name)
    assert loaded_port is not None
    assert loaded_port.hint == port.hint
    assert loaded_port.type == port.type
    
    if os.path.exists(file_name):
        os.remove(file_name)

def test_load_wrong_file():
    """Test loading file with wrong format."""
    with open("/tmp/wrong.json", "w") as f:
        f.write('{"data": "PORT", "type": "invalid", "version": "1.0", "language": "invalid", "hint": "", "color": "#000", "multiple": false, "var_name": "test", "code": "invalid"}')  # JSON com todos os campos mas dados inválidos
    result = PortPersistence.load("/tmp/wrong.json")
    assert result is None
    os.remove("/tmp/wrong.json")

def test_save_no_permission(port):
    """Test saving without permission."""
    result = PortPersistence.save(port, "/root/")
    assert result is False


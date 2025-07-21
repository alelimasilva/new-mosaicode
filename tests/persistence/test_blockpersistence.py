# Migrated from unittest/TestBase to pytest.
import os
import pytest
from mosaicode.utils.FileUtils import *
from mosaicode.model.blockmodel import BlockModel
from mosaicode.model.port import Port
from mosaicode.persistence.blockpersistence import BlockPersistence

def test_load_non_existent():
    """Test loading non-existent file."""
    result = BlockPersistence.load("/tmp/nonexistent.json")
    assert result is None

def test_load_save(block):
    """Test load and save functionality."""
    BlockPersistence.save(block, "/tmp/")
    file_name = "/tmp/" + block.type + ".json"
    result = BlockPersistence.load(file_name)
    assert result is not None
    if os.path.exists(file_name):
        os.remove(file_name)

def test_load_wrong_file():
    """Test loading file with wrong format."""
    with open("/tmp/wrong.json", "w") as f:
        f.write("not a block")
    result = BlockPersistence.load("/tmp/wrong.json")
    assert result is None
    os.remove("/tmp/wrong.json")

def test_save_no_permission(block):
    """Test saving without permission."""
    result = BlockPersistence.save(block, "/root/")
    assert result is False

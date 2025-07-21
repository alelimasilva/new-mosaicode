# -*- coding: utf-8 -*-
"""
Tests for BlockModel (pure logic, no GUI dependencies).
"""
from pathlib import Path
import tempfile
import shutil
import json
import pytest

from mosaicode.model.blockmodel import BlockModel

@pytest.fixture
def temp_dir():
    dir_path = Path(tempfile.mkdtemp(prefix="mosaicode_test_"))
    yield dir_path
    if dir_path.exists():
        shutil.rmtree(dir_path)

def test_block_creation():
    block = BlockModel()
    assert block.id == -1
    assert block.x == 0
    assert block.y == 0
    assert not block.is_collapsed
    assert block.label == "A"
    assert block.color == "#000000"
    assert block.group == "Undefined"

def test_block_with_custom_values():
    block = BlockModel(
        id=1,
        x=100,
        y=200,
        label="Test Block",
        color="#FF0000",
        group="Test Group"
    )
    assert block.id == 1
    assert block.x == 100
    assert block.y == 200
    assert block.label == "Test Block"
    assert block.color == "#FF0000"
    assert block.group == "Test Group"

def test_block_properties():
    block = BlockModel()
    assert isinstance(block.properties, list)
    assert len(block.properties) == 0
    
    # Test adding properties
    block.properties.append({"name": "test", "value": "value"})
    assert len(block.properties) == 1
    assert block.properties[0]["name"] == "test"

def test_block_ports():
    block = BlockModel()
    assert isinstance(block.ports, list)
    assert len(block.ports) == 0
    
    # Test adding ports
    port = {"type": "input", "name": "test_port"}
    block.ports.append(port)
    assert len(block.ports) == 1
    assert block.ports[0]["type"] == "input"

def test_block_codes():
    block = BlockModel()
    assert isinstance(block.codes, dict)
    assert len(block.codes) == 0
    
    # Test adding codes
    block.codes["function"] = "print('test')"
    assert len(block.codes) == 1
    assert block.codes["function"] == "print('test')"

def test_block_validation():
    block = BlockModel()
    # Basic validation - should not raise exceptions
    assert block.id >= -1
    assert isinstance(block.label, str)
    assert isinstance(block.color, str)
    assert isinstance(block.group, str)

def test_block_serialization(temp_dir):
    block = BlockModel(
        id=1,
        label="Test Block",
        color="#FF0000",
        group="Test Group"
    )
    
    # Test basic serialization using dataclass fields
    block_dict = {
        "id": block.id,
        "label": block.label,
        "color": block.color,
        "group": block.group,
        "type": block.type,
        "version": block.version
    }
    
    assert isinstance(block_dict, dict)
    assert block_dict["id"] == 1
    assert block_dict["label"] == "Test Block"
    assert block_dict["color"] == "#FF0000"
    
    # Test creating new block with same values
    new_block = BlockModel(**block_dict)
    assert new_block.id == block.id
    assert new_block.label == block.label
    assert new_block.color == block.color 
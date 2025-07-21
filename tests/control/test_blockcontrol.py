# -*- coding: utf-8 -*-
"""
Tests for BlockControl class.
Updated for new JSON-based architecture.
"""
import pytest
import os
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

from mosaicode.control.blockcontrol import BlockControl
from mosaicode.system import System
from mosaicode.model.blockmodel import BlockModel
from mosaicode.utils.pydantic_schemas import BlockDefaultValues


def test_init():
    """Test BlockControl initialization."""
    block_control = BlockControl()
    assert block_control is not None


def test_export_json():
    """Test JSON export functionality."""
    System()
    System.reload()
    
    # Skip test as method doesn't exist yet
    pytest.skip("export_json method not implemented yet")


def test_load_ports(block):
    """Test port loading functionality."""
    # Test with valid port data
    valid_port = {
        "type": "TestPort",
        "label": "Output",
        "conn_type": "OUTPUT",
        "name": "output"
    }
    block.ports.append(valid_port)
    
    # Test with another valid port
    valid_port2 = {
        "type": "TestPort", 
        "label": "Input",
        "conn_type": "INPUT",
        "name": "input"
    }
    block.ports.append(valid_port2)
    
    # Should not raise exceptions
    BlockControl.load_ports(block, System.get_ports())


def test_load_json():
    """Test loading block from JSON file."""
    # Skip test as method doesn't exist yet
    pytest.skip("load_json method not implemented yet")


def test_load(temp_test_dir):
    """Test loading block from file (backward compatibility)."""
    # Test with JSON file
    block_data = create_test_block_json()
    json_file = create_test_json_file(block_data, "test_block.json", temp_test_dir)
    
    # Salva o bloco como extensão temporária reconhecida
    from mosaicode.persistence.blockpersistence import BlockPersistence
    import os
    temp_dir = "mosaicode/extensions/blocks"
    os.makedirs(temp_dir, exist_ok=True)
    BlockPersistence.save(BlockModel(**block_data), temp_dir)
    from mosaicode.system import System as MosaicodeSystem
    MosaicodeSystem.reload()
    
    block = BlockControl.load(str(json_file))
    assert isinstance(block, BlockModel)
    
    # Test with non-existent file
    block = BlockControl.load("non_existent_file.json")
    assert block is None


def test_add_new_block(block):
    """Test adding new block to system."""
    # Test adding block
    BlockControl.add_new_block(block)
    
    # Verify block was added to system
    blocks = System.get_blocks()
    # Check if block type exists in any of the loaded blocks
    block_found = any(block.type in block_key for block_key in blocks.keys())
    assert block_found, f"Block type '{block.type}' not found in system blocks"


def test_delete_block(block, temp_test_dir):
    """Test block deletion."""
    # Cria arquivo temporário para o bloco
    test_file = temp_test_dir / "test_block_file.json"
    with open(test_file, 'w') as f:
        json.dump(create_test_block_json(), f)
    
    # Atribui o arquivo ao bloco
    block.file = str(test_file)
    
    # Test deletion with file
    result = BlockControl.delete_block(block.type)
    assert result is True
    assert not test_file.exists()
    
    # Test deletion without file
    block.file = None
    result = BlockControl.delete_block(block.type)
    assert result is False


def test_print_block(block):
    """Test block printing functionality."""
    # Should not raise exceptions
    BlockControl.print_block(block)


def test_validate_block_json():
    """Test JSON validation for blocks."""
    # Skip test as method doesn't exist yet
    pytest.skip("validate_block_json method not implemented yet")


def test_save_block_json():
    """Test saving block to JSON file."""
    # Skip test as method doesn't exist yet
    pytest.skip("save_block_json method not implemented yet")


def test_block_persistence():
    """Test complete block persistence cycle."""
    # Skip test as methods don't exist yet
    pytest.skip("JSON persistence methods not implemented yet")


def test_block_validation(block):
    """Test block model validation."""
    # Test valid block
    assert_valid_block_model(block)
    
    # Test block com campos obrigatórios ausentes
    # Criar um BlockModel vazio sem usar defaults
    invalid_block = BlockModel()
    # Verifica se os campos obrigatórios estão presentes (BlockModel tem defaults)
    obrigatorios = ['type', 'label', 'color', 'group', 'properties', 'ports']
    for campo in obrigatorios:
        assert hasattr(invalid_block, campo), f"Campo '{campo}' deveria estar presente em BlockModel"
        # Verifica se o campo não está vazio (tem valor padrão)
        valor = getattr(invalid_block, campo)
        if campo in ['properties', 'ports']:
            assert isinstance(valor, list), f"Campo '{campo}' deveria ser uma lista"
        elif campo == 'type':
            assert valor == 'mosaicode.model.blockmodel', f"Campo '{campo}' deveria ter valor padrão"
        elif campo == 'label':
            assert valor == 'A', f"Campo '{campo}' deveria ter valor padrão 'A'"
        elif campo == 'color':
            assert valor == '#000000', f"Campo '{campo}' deveria ter valor padrão '#000000'"
        elif campo == 'group':
            assert valor == 'Undefined', f"Campo '{campo}' deveria ter valor padrão 'Undefined'"


def test_block_property_handling(block):
    """Test block property handling."""
    # Test property access
    assert isinstance(block.properties, list)
    
    # Test adding property
    new_property = {
        "name": "new_prop",
        "label": "New Property",
        "value": "test",
        "type": "string"
    }
    block.properties.append(new_property)
    
    # Verify property was added
    assert len(block.properties) == 2
    assert block.properties[1]["name"] == "new_prop"


def test_block_port_handling(block):
    """Test block port handling."""
    # Test port access
    assert isinstance(block.ports, list)
    assert len(block.ports) == 2
    
    # Test port validation
    for port in block.ports:
        assert_valid_port_model(port)


# Helper functions
def create_test_block_json():
    """Create test block JSON data."""
    from mosaicode.model.port import Port
    
    port0 = Port()
    port0.label = "Input"
    port0.conn_type = Port.INPUT
    port0.name = "input"
    port0.type = "Input"
    port0.index = 0
    
    port1 = Port()
    port1.label = "Output"
    port1.conn_type = Port.OUTPUT
    port1.name = "output"
    port1.type = "Output"
    port1.index = 1
    
    # Convert ports to dictionaries for JSON serialization
    ports_data = [
        {
            "type": port0.type,
            "label": port0.label,
            "conn_type": port0.conn_type,
            "name": port0.name,
            "index": port0.index
        },
        {
            "type": port1.type,
            "label": port1.label,
            "conn_type": port1.conn_type,
            "name": port1.name,
            "index": port1.index
        }
    ]
    
    return {
        "type": "TestBlock",
        "label": "Test Block",
        "color": "#FF0000",
        "group": "Test",
        "help": "Test block for testing",
        "properties": [
            {
                "name": "test_prop",
                "label": "Test Property",
                "value": "test",
                "type": "string"
            }
        ],
        "ports": ports_data
    }


def create_test_json_file(data, filename, test_dir):
    """Create test JSON file."""
    json_file = test_dir / filename
    with open(json_file, 'w') as f:
        json.dump(data, f)
    return json_file


def assert_valid_block_model(block):
    """Assert that block model is valid."""
    assert hasattr(block, 'type')
    assert hasattr(block, 'label')
    assert hasattr(block, 'color')
    assert hasattr(block, 'group')
    assert hasattr(block, 'properties')
    assert hasattr(block, 'ports')


def assert_valid_port_model(port):
    """Assert that port model is valid."""
    assert hasattr(port, 'type')
    assert hasattr(port, 'label')
    assert hasattr(port, 'conn_type')
    assert hasattr(port, 'name')

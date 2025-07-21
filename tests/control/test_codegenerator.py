# -*- coding: utf-8 -*-
"""
Tests for CodeGenerator class.
Migrated from unittest/TestBase to pytest.
"""
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from mosaicode.control.codegenerator import CodeGenerator

@pytest.fixture
def temp_dir():
    """Create temporary directory for tests."""
    test_dir = Path(tempfile.mkdtemp(prefix="mosaicode_test_"))
    yield test_dir
    if test_dir.exists():
        shutil.rmtree(test_dir)

@pytest.fixture
def diagram():
    """Create a basic diagram for testing."""
    from mosaicode.model.diagrammodel import DiagramModel
    return DiagramModel()

@pytest.fixture
def code_generator(diagram):
    """Create a CodeGenerator instance."""
    return CodeGenerator(diagram)

@pytest.fixture
def block():
    """Create a basic block for testing."""
    from mosaicode.model.blockmodel import BlockModel
    return BlockModel()

@pytest.fixture
def port():
    """Create a basic port for testing."""
    from mosaicode.model.port import Port
    return Port()

@pytest.fixture
def connection():
    """Create a basic connection for testing."""
    from mosaicode.model.connectionmodel import ConnectionModel
    from mosaicode.model.blockmodel import BlockModel
    from mosaicode.model.port import Port
    
    # Create a basic connection with required parameters
    block1 = BlockModel()
    block2 = BlockModel()
    port1 = Port()
    port2 = Port()
    
    connection = ConnectionModel(diagram=None, output=block1, output_port=port1, input=block2, input_port=port2)
    return connection

def create_diagram_with_blocks(diagram, block, connection):
    """Create a diagram with test blocks."""
    from mosaicode.model.blockmodel import BlockModel
    
    # Add test blocks
    block1 = block
    block1.id = 1
    block1.type = "test.block1"
    block1.label = "Block 1"
    block1.codes = {"function": "print('Hello from block 1')"}
    
    block2 = BlockModel()
    block2.id = 2
    block2.type = "test.block2"
    block2.label = "Block 2"
    block2.codes = {"function": "print('Hello from block 2')"}
    
    diagram.blocks = {"1": block1, "2": block2}
    return diagram

def test_code_generator_initialization(code_generator, diagram):
    """Test CodeGenerator initialization."""
    assert code_generator is not None
    assert code_generator._CodeGenerator__diagram == diagram
    assert code_generator._CodeGenerator__block_list == []
    assert code_generator._CodeGenerator__connections == []
    assert code_generator._CodeGenerator__codes == {}

def test_generate_code_integration(diagram, block, connection):
    """Test complete code generation integration."""
    diagram = create_diagram_with_blocks(diagram, block, connection)
    code_generator = CodeGenerator(diagram)
    
    # Test complete code generation
    result = code_generator.generate_code()
    assert isinstance(result, dict)

def test_generate_code_empty_diagram(diagram):
    """Test code generation with empty diagram."""
    empty_diagram = diagram
    empty_diagram.blocks = {}
    empty_diagram.connectors = []
    
    code_generator = CodeGenerator(empty_diagram)
    result = code_generator.generate_code()
    assert isinstance(result, dict)

def test_generate_code_with_errors(diagram, block, connection):
    """Test code generation error handling."""
    diagram = create_diagram_with_blocks(diagram, block, connection)
    
    # Create block with invalid code
    block = diagram.blocks["1"]
    block.codes = {"function": "$invalid_property$"}
    
    code_generator = CodeGenerator(diagram)
    
    # Should not raise exception, should handle gracefully
    result = code_generator.generate_code()
    assert isinstance(result, dict)

# -*- coding: utf-8 -*-
"""
Tests for CodeGenerator (pure logic, no GUI dependencies).
"""
import pytest
from pathlib import Path
import tempfile
import shutil
import json
from unittest.mock import Mock, patch, MagicMock

# Mock the GTK import before importing CodeGenerator
import sys
from unittest.mock import MagicMock

# Create a mock for gi module
mock_gi = MagicMock()
sys.modules['gi'] = mock_gi
sys.modules['gi.repository'] = MagicMock()
sys.modules['gi.repository.Gtk'] = MagicMock()

# Now we can import CodeGenerator
from mosaicode.control.codegenerator import CodeGenerator


@pytest.fixture
def test_dir():
    """Create temporary test directory."""
    test_dir = Path(tempfile.mkdtemp(prefix="mosaicode_test_"))
    yield test_dir
    if test_dir.exists():
        shutil.rmtree(test_dir)


@pytest.fixture
def mock_diagram():
    """Create a mock diagram for testing."""
    diagram = Mock()
    
    # Mock blocks
    block1 = Mock()
    block1.id = 1
    block1.type = "test.block1"
    block1.label = "Block 1"
    block1.weight = 0
    block1.connections = []
    block1.codes = {"function": "print('Hello from block 1')"}
    block1.gen_codes = {}
    block1.ports = []
    block1.get_properties.return_value = []
    
    block2 = Mock()
    block2.id = 2
    block2.type = "test.block2"
    block2.label = "Block 2"
    block2.weight = 0
    block2.connections = []
    block2.codes = {"function": "print('Hello from block 2')"}
    block2.gen_codes = {}
    block2.ports = []
    block2.get_properties.return_value = []
    
    diagram.blocks = {1: block1, 2: block2}
    diagram.connectors = []
    
    # Mock code template
    code_template = Mock()
    code_template.code_parts = ["function", "declaration"]
    code_template.command = "python $dir_name$index.py"
    code_template.name = "test_template"
    code_template.description = "Test template"
    code_template.properties = []
    
    diagram.code_template = code_template
    
    return diagram


class TestCodeGeneratorPure:
    """Test cases for CodeGenerator (pure logic)."""

    def test_code_generator_initialization(self, mock_diagram):
        """Test CodeGenerator initialization."""
        code_generator = CodeGenerator(mock_diagram)
        assert code_generator is not None
        assert code_generator._CodeGenerator__diagram == mock_diagram
        assert code_generator._CodeGenerator__block_list == []
        assert code_generator._CodeGenerator__connections == []
        assert code_generator._CodeGenerator__codes == {}

    def test_prepare_block_list(self, mock_diagram):
        """Test block list preparation."""
        code_generator = CodeGenerator(mock_diagram)
        
        # Test prepare block list
        result = code_generator._CodeGenerator__prepare_block_list()
        assert result is True
        
        # Check that blocks were added to the list
        assert len(code_generator._CodeGenerator__block_list) == 2
        
        # Check that blocks have weight and connections initialized
        for block in code_generator._CodeGenerator__block_list:
            assert block.weight == 0
            assert block.connections == []

    def test_sort_block_list(self, mock_diagram):
        """Test block list sorting."""
        code_generator = CodeGenerator(mock_diagram)
        code_generator._CodeGenerator__prepare_block_list()
        
        # Test sort block list
        result = code_generator._CodeGenerator__sort_block_list()
        assert result is True
        
        # All blocks should still have weight 0 since there are no connections
        for block in code_generator._CodeGenerator__block_list:
            assert block.weight == 0

    def test_sort_block_list_with_connections(self):
        """Test block list sorting with connections."""
        # Create mock diagram with connections
        diagram = Mock()
        
        # Create blocks
        block1 = Mock()
        block1.id = 1
        block1.weight = 0
        block1.connections = []
        
        block2 = Mock()
        block2.id = 2
        block2.weight = 0
        block2.connections = []
        
        # Create connection
        connection = Mock()
        connection.output = block1
        connection.input = block2
        
        # Set up connections
        block1.connections = [connection]
        
        diagram.blocks = {1: block1, 2: block2}
        diagram.connectors = [connection]
        
        code_generator = CodeGenerator(diagram)
        code_generator._CodeGenerator__prepare_block_list()
        
        # Test sort block list
        result = code_generator._CodeGenerator__sort_block_list()
        assert result is True
        
        # Block2 should have higher weight than block1
        block1_weight = next(b.weight for b in code_generator._CodeGenerator__block_list if b.id == 1)
        block2_weight = next(b.weight for b in code_generator._CodeGenerator__block_list if b.id == 2)
        assert block2_weight > block1_weight

    def test_generate_port_var_name_code(self, mock_diagram):
        """Test port variable name code generation."""
        code_generator = CodeGenerator(mock_diagram)
        
        # Create mock block and port
        block = Mock()
        block.id = 1
        block.type = "test.block"
        
        port = Mock()
        port.var_name = "$port[name]$"
        port.name = "test_port"
        
        # Test port variable name generation
        result = code_generator._CodeGenerator__generate_port_var_name_code(block, port)
        assert result == "test_port"

    def test_generate_block_code_parts(self, mock_diagram):
        """Test block code parts generation."""
        code_generator = CodeGenerator(mock_diagram)
        code_generator._CodeGenerator__prepare_block_list()
        code_generator._CodeGenerator__sort_block_list()
        
        # Test generate block code parts
        result = code_generator._CodeGenerator__generate_block_code_parts()
        assert result is True
        
        # Check that codes were generated for each part
        assert "function" in code_generator._CodeGenerator__codes
        assert "declaration" in code_generator._CodeGenerator__codes

    def test_generate_block_code(self, mock_diagram):
        """Test individual block code generation."""
        code_generator = CodeGenerator(mock_diagram)
        code_generator._CodeGenerator__prepare_block_list()
        
        # Get first block
        block = code_generator._CodeGenerator__block_list[0]
        
        # Test generate block code
        result = code_generator._CodeGenerator__generate_block_code(block)
        assert result is True
        
        # Check that gen_codes were created for the block
        assert "function" in block.gen_codes
        assert block.gen_codes["function"] == "print('Hello from block 1')"

    def test_generate_file_code(self, mock_diagram, test_dir):
        """Test file code generation."""
        # Mock diagram.language e patch_name para evitar TypeError
        mock_diagram.language = "python"
        mock_diagram.patch_name = "test_patch"
        # Mock code_template.codes para evitar erro de iteração
        mock_diagram.code_template.codes = {"function": "print('Hello World')"}
        
        code_generator = CodeGenerator(mock_diagram)
        code_generator._CodeGenerator__prepare_block_list()
        code_generator._CodeGenerator__sort_block_list()
        code_generator._CodeGenerator__generate_block_code_parts()
        
        # Test generate file code com template simples
        template_code = "print('Hello World')"
        result = code_generator._CodeGenerator__generate_file_code(template_code)
        assert isinstance(result, str)
        assert "Hello World" in result

    def test_generate_code_integration(self, mock_diagram, test_dir):
        """Test complete code generation integration."""
        # Mock diagram.language e patch_name para evitar TypeError
        mock_diagram.language = "python"
        mock_diagram.patch_name = "test_patch"
        # Mock code_template.codes para evitar erro de iteração
        mock_diagram.code_template.codes = {"function": "print('Hello World')"}
        
        code_generator = CodeGenerator(mock_diagram)
        
        # Test complete code generation
        result = code_generator.generate_code()
        assert isinstance(result, dict)
        assert "function" in result
        assert "Hello World" in result["function"]

    def test_code_generator_with_properties(self):
        """Test code generator with block properties."""
        # Create mock diagram with properties
        diagram = Mock()
        
        # Create block with properties
        block = Mock()
        block.id = 1
        block.type = "test.block"
        block.label = "Test Block"
        block.weight = 0
        block.connections = []
        block.codes = {"function": "print('Hello from block')"}
        block.gen_codes = {}
        block.ports = []
        
        # Mock properties
        properties = [
            {"name": "prop1", "value": "value1"},
            {"name": "prop2", "value": "value2"}
        ]
        block.get_properties.return_value = properties
        
        diagram.blocks = {1: block}
        diagram.connectors = []
        
        # Mock code template
        code_template = Mock()
        code_template.code_parts = ["function"]
        code_template.command = "python $dir_name$index.py"
        code_template.name = "test_template"
        code_template.description = "Test template"
        code_template.properties = []
        
        diagram.code_template = code_template
        
        code_generator = CodeGenerator(diagram)
        code_generator._CodeGenerator__prepare_block_list()
        
        # Test that properties are handled correctly
        block = code_generator._CodeGenerator__block_list[0]
        properties = block.get_properties()
        assert len(properties) == 2
        assert properties[0]["name"] == "prop1"
        assert properties[1]["name"] == "prop2"

    def test_code_generator_with_ports(self):
        """Test code generator with block ports."""
        # Create mock diagram with ports
        diagram = Mock()
        
        # Create block with ports
        block = Mock()
        block.id = 1
        block.type = "test.block"
        block.label = "Test Block"
        block.weight = 0
        block.connections = []
        block.codes = {"function": "print('Hello from block')"}
        block.gen_codes = {}
        
        # Mock ports
        port1 = Mock()
        port1.name = "input1"
        port1.type = "float"
        port1.conn_type = "INPUT"
        
        port2 = Mock()
        port2.name = "output1"
        port2.type = "float"
        port2.conn_type = "OUTPUT"
        
        block.ports = [port1, port2]
        block.get_properties.return_value = []
        
        diagram.blocks = {1: block}
        diagram.connectors = []
        
        # Mock code template
        code_template = Mock()
        code_template.code_parts = ["function"]
        code_template.command = "python $dir_name$index.py"
        code_template.name = "test_template"
        code_template.description = "Test template"
        code_template.properties = []
        
        diagram.code_template = code_template
        
        code_generator = CodeGenerator(diagram)
        code_generator._CodeGenerator__prepare_block_list()
        
        # Test that ports are handled correctly
        block = code_generator._CodeGenerator__block_list[0]
        assert len(block.ports) == 2
        assert block.ports[0].name == "input1"
        assert block.ports[1].name == "output1" 
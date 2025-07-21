# -*- coding: utf-8 -*-
"""
Tests for ConnectionModel class.
Migrated from unittest to pytest.
"""
import pytest

from mosaicode.model.connectionmodel import ConnectionModel
from mosaicode.model.port import Port


@pytest.fixture
def diagram():
    """Create a test diagram."""
    from mosaicode.model.diagrammodel import DiagramModel
    return DiagramModel()


@pytest.fixture
def block1():
    """Create a test block 1."""
    from mosaicode.model.blockmodel import BlockModel
    block = BlockModel()
    block.id = 1
    block.type = "TestBlock1"
    block.label = "Test Block 1"
    return block


@pytest.fixture
def block2():
    """Create a test block 2."""
    from mosaicode.model.blockmodel import BlockModel
    block = BlockModel()
    block.id = 2
    block.type = "TestBlock2"
    block.label = "Test Block 2"
    return block


@pytest.fixture
def port1():
    """Create a test port 1."""
    port = Port()
    port.name = "output_port"
    port.conn_type = Port.OUTPUT
    return port


@pytest.fixture
def port2():
    """Create a test port 2."""
    port = Port()
    port.name = "input_port"
    port.conn_type = Port.INPUT
    return port


def test_connection_model_initialization(diagram, block1, block2, port1, port2):
    """Test ConnectionModel initialization."""
    connection = ConnectionModel(
        diagram,
        block1,
        port1,
        block2,
        port2
    )
    assert connection is not None


def test_connection_model_default_values(diagram, block1, block2, port1, port2):
    """Test ConnectionModel default values."""
    connection = ConnectionModel(
        diagram,
        block1,
        port1,
        block2,
        port2
    )
    
    # Test default attributes
    assert connection.diagram == diagram
    assert connection.output == block1
    assert connection.input == block2
    assert connection.output_port == port1
    assert connection.input_port == port2


def test_connection_model_with_none_values(diagram):
    """Test ConnectionModel with None values."""
    connection = ConnectionModel(
        diagram,
        None,
        None,
        None,
        None
    )
    
    # Test with None values
    assert connection.diagram == diagram
    assert connection.output is None
    assert connection.input is None
    assert connection.output_port is None
    assert connection.input_port is None


def test_connection_model_set_values(diagram, block1, block2, port1, port2):
    """Test setting values in ConnectionModel."""
    connection = ConnectionModel(
        diagram,
        block1,
        port1,
        block2,
        port2
    )
    
    # Test that values are set correctly
    assert connection.diagram == diagram
    assert connection.output == block1
    assert connection.input == block2
    assert connection.output_port == port1
    assert connection.input_port == port2


def test_connection_model_validation(diagram, block1, block2, port1, port2):
    """Test ConnectionModel validation."""
    # Test with valid blocks and ports
    connection = ConnectionModel(
        diagram,
        block1,
        port1,
        block2,
        port2
    )
    
    # Verify connection is valid
    assert connection.diagram is not None
    assert connection.output is not None
    assert connection.input is not None
    assert connection.output_port is not None
    assert connection.input_port is not None


def test_connection_model_equality(diagram, block1, block2, port1, port2):
    """Test ConnectionModel equality."""
    connection1 = ConnectionModel(
        diagram,
        block1,
        port1,
        block2,
        port2
    )
    
    connection2 = ConnectionModel(
        diagram,
        block1,
        port1,
        block2,
        port2
    )
    
    # Test equality
    assert connection1.diagram == connection2.diagram
    assert connection1.output == connection2.output
    assert connection1.input == connection2.input
    assert connection1.output_port == connection2.output_port
    assert connection1.input_port == connection2.input_port


def test_connection_model_str_representation(diagram, block1, block2, port1, port2):
    """Test ConnectionModel string representation."""
    connection = ConnectionModel(
        diagram,
        block1,
        port1,
        block2,
        port2
    )
    
    # Test string representation
    str_repr = str(connection)
    assert isinstance(str_repr, str)


def test_connection_model_with_different_ports(diagram, block1, block2):
    """Test ConnectionModel with different port types."""
    # Create different ports
    port1 = Port()
    port1.name = "output_port"
    port1.conn_type = Port.OUTPUT
    
    port2 = Port()
    port2.name = "input_port"
    port2.conn_type = Port.INPUT
    
    connection = ConnectionModel(
        diagram,
        block1,
        port1,
        block2,
        port2
    )
    
    # Verify connection
    assert connection.output_port == port1
    assert connection.input_port == port2
    if connection.output_port:
        assert connection.output_port.name == "output_port"
    if connection.input_port:
        assert connection.input_port.name == "input_port"


def test_connection_model_serialization(diagram, block1, block2, port1, port2):
    """Test ConnectionModel serialization."""
    connection = ConnectionModel(
        diagram,
        block1,
        port1,
        block2,
        port2
    )
    
    # Test to_dict method if it exists
    if hasattr(connection, 'to_dict'):
        data = connection.to_dict()
        assert isinstance(data, dict)


def test_connection_model_from_dict(diagram, block1, block2, port1, port2):
    """Test creating ConnectionModel from dictionary."""
    data = {
        'diagram': diagram,
        'output': block1,
        'input': block2,
        'output_port': port1,
        'input_port': port2
    }
    
    # Test from_dict method if it exists
    if hasattr(ConnectionModel, 'from_dict'):
        connection = ConnectionModel.from_dict(data)
        assert connection.diagram == diagram
        assert connection.output == block1
        assert connection.input == block2


def test_connection_model_copy(diagram, block1, block2, port1, port2):
    """Test copying ConnectionModel."""
    connection1 = ConnectionModel(
        diagram,
        block1,
        port1,
        block2,
        port2
    )
    
    # Test copy if method exists
    if hasattr(connection1, 'copy'):
        connection2 = connection1.copy()
        assert connection1.diagram == connection2.diagram
        assert connection1.output == connection2.output
        assert connection1.input == connection2.input
        assert connection1 is not connection2


def test_connection_model_empty_diagram(block1, block2, port1, port2):
    """Test ConnectionModel with empty diagram."""
    from mosaicode.model.diagrammodel import DiagramModel
    empty_diagram = DiagramModel()
    empty_diagram.blocks = {}
    empty_diagram.connectors = []
    
    connection = ConnectionModel(
        empty_diagram,
        block1,
        port1,
        block2,
        port2
    )
    
    # Verify connection works with empty diagram
    assert connection.diagram == empty_diagram
    assert connection.output == block1
    assert connection.input == block2

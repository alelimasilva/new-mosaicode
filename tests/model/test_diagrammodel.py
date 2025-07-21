# -*- coding: utf-8 -*-
"""
Tests for DiagramModel class.
Migrated from unittest to pytest.
"""
import pytest
from pathlib import Path

from mosaicode.model.diagrammodel import DiagramModel
from mosaicode.model.blockmodel import BlockModel
from mosaicode.model.commentmodel import CommentModel


@pytest.fixture
def diagram():
    """Create a test diagram."""
    return DiagramModel()


@pytest.fixture
def test_block():
    """Create a test block."""
    block = BlockModel()
    block.id = 1
    block.type = "TestBlock"
    block.label = "Test Block"
    return block


@pytest.fixture
def test_comment():
    """Create a test comment."""
    comment = CommentModel()
    comment.id = 1
    comment.x = 100
    comment.y = 100
    return comment


def test_diagram_model_initialization(diagram):
    """Test DiagramModel initialization."""
    assert diagram is not None


def test_diagram_model_default_values(diagram):
    """Test DiagramModel default values."""
    # Test default attributes
    assert diagram.last_id == 1
    assert diagram.blocks == {}
    assert diagram.connectors == []
    assert diagram.comments == []
    assert diagram.code_template is None
    assert diagram.zoom == 1.0
    assert diagram.file_name == "Untitled"
    assert diagram.modified is False
    assert diagram.language is None
    assert diagram.undo_stack == []
    assert diagram.redo_stack == []
    assert diagram.authors == []


def test_diagram_model_set_values(diagram):
    """Test setting values in DiagramModel."""
    # Set values
    diagram.last_id = 5
    diagram.file_name = "test.mscd"
    diagram.zoom = 2.0
    diagram.modified = True
    diagram.language = "python"
    
    # Verify values
    assert diagram.last_id == 5
    assert diagram.file_name == "test.mscd"
    assert diagram.zoom == 2.0
    assert diagram.modified is True
    assert diagram.language == "python"


def test_patch_name_property(diagram):
    """Test patch_name property."""
    # Test with simple filename
    diagram.file_name = "test.mscd"
    assert diagram.patch_name == "test"
    
    # Test with path
    diagram.file_name = "/path/to/test.mscd"
    assert diagram.patch_name == "test"
    
    # Test with Windows path - the current implementation returns the full path stem
    diagram.file_name = "C:\\path\\to\\test.mscd"
    assert diagram.patch_name == "C:\\path\\to\\test"
    
    # Test with no extension
    diagram.file_name = "test"
    assert diagram.patch_name == "test"


def test_diagram_model_str_representation(diagram):
    """Test DiagramModel string representation."""
    diagram.file_name = "test.mscd"
    
    # Test string representation
    str_repr = str(diagram)
    assert str_repr == "test"


def test_diagram_model_with_blocks(diagram, test_block):
    """Test DiagramModel with blocks."""
    # Add blocks
    block1 = test_block
    block2 = BlockModel()
    block2.id = 2
    block2.type = "TestBlock2"
    block2.label = "Test Block 2"
    
    diagram.blocks = {"1": block1, "2": block2}
    
    # Verify blocks
    assert len(diagram.blocks) == 2
    assert "1" in diagram.blocks
    assert "2" in diagram.blocks
    assert diagram.blocks["1"] == block1
    assert diagram.blocks["2"] == block2


def test_diagram_model_with_connectors(diagram):
    """Test DiagramModel with connectors."""
    # Add connectors (using mock objects)
    connector1 = object()
    connector2 = object()
    
    diagram.connectors = [connector1, connector2]
    
    # Verify connectors
    assert len(diagram.connectors) == 2
    assert connector1 in diagram.connectors
    assert connector2 in diagram.connectors


def test_diagram_model_with_comments(diagram, test_comment):
    """Test DiagramModel with comments."""
    # Add comments
    comment1 = test_comment
    comment2 = CommentModel()
    comment2.id = 2
    comment2.x = 200
    comment2.y = 200
    
    diagram.comments = [comment1, comment2]
    
    # Verify comments
    assert len(diagram.comments) == 2
    assert comment1 in diagram.comments
    assert comment2 in diagram.comments


def test_diagram_model_with_authors(diagram):
    """Test DiagramModel with authors."""
    # Add authors
    diagram.authors = ["Author 1", "Author 2"]
    
    # Verify authors
    assert len(diagram.authors) == 2
    assert "Author 1" in diagram.authors
    assert "Author 2" in diagram.authors


def test_diagram_model_with_undo_redo(diagram):
    """Test DiagramModel with undo/redo stacks."""
    # Add to undo stack
    diagram.undo_stack = ["action1", "action2"]
    diagram.redo_stack = ["redo1"]
    
    # Verify stacks
    assert len(diagram.undo_stack) == 2
    assert len(diagram.redo_stack) == 1
    assert "action1" in diagram.undo_stack
    assert "action2" in diagram.undo_stack
    assert "redo1" in diagram.redo_stack


def test_diagram_model_serialization(diagram):
    """Test DiagramModel serialization."""
    diagram.file_name = "test.mscd"
    diagram.language = "python"
    diagram.modified = True
    
    # Test to_dict method if it exists
    if hasattr(diagram, 'to_dict'):
        data = diagram.to_dict()
        assert isinstance(data, dict)
        assert data.get('file_name') == "test.mscd"
        assert data.get('language') == "python"
        assert data.get('modified') is True


def test_diagram_model_from_dict():
    """Test creating DiagramModel from dictionary."""
    data = {
        'file_name': 'test.mscd',
        'language': 'python',
        'modified': True,
        'zoom': 2.0,
        'last_id': 5
    }
    
    # Test from_dict method if it exists
    if hasattr(DiagramModel, 'from_dict'):
        diagram = DiagramModel.from_dict(data)
        assert diagram.file_name == "test.mscd"
        assert diagram.language == "python"
        assert diagram.modified is True
        assert diagram.zoom == 2.0
        assert diagram.last_id == 5


def test_diagram_model_copy(diagram):
    """Test copying DiagramModel."""
    diagram.file_name = "test.mscd"
    diagram.language = "python"
    
    # Test copy if method exists
    if hasattr(diagram, 'copy'):
        diagram2 = diagram.copy()
        assert diagram.file_name == diagram2.file_name
        assert diagram.language == diagram2.language
        assert diagram is not diagram2


def test_diagram_model_empty_values(diagram):
    """Test DiagramModel with empty values."""
    # Test setting empty values
    diagram.file_name = ""
    diagram.language = ""
    diagram.authors = []
    
    # Verify empty values are accepted
    assert diagram.file_name == ""
    assert diagram.language == ""
    assert diagram.authors == []
    assert diagram.patch_name == ""


def test_diagram_model_special_characters(diagram):
    """Test DiagramModel with special characters."""
    # Test with special characters
    diagram.file_name = "testé.mscd"
    diagram.language = "pythön"
    
    # Verify special characters are preserved
    assert diagram.file_name == "testé.mscd"
    assert diagram.language == "pythön"
    assert diagram.patch_name == "testé"


def test_diagram_model_edge_cases(diagram):
    """Test DiagramModel edge cases."""
    # Test with very long filename
    long_filename = "a" * 1000 + ".mscd"
    diagram.file_name = long_filename
    assert diagram.file_name == long_filename
    
    # Test with filename without extension
    diagram.file_name = "noextension"
    assert diagram.patch_name == "noextension"
    
    # Test with filename with multiple dots
    diagram.file_name = "test.file.mscd"
    assert diagram.patch_name == "test.file"

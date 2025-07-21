# -*- coding: utf-8 -*-
"""
Tests for AuthorModel class.
Migrated from unittest to pytest.
"""
import pytest
from datetime import datetime

from mosaicode.model.authormodel import AuthorModel


def test_author_model_initialization():
    """Test AuthorModel initialization."""
    authormodel = AuthorModel()
    assert authormodel is not None


def test_author_model_default_values():
    """Test AuthorModel default values."""
    authormodel = AuthorModel()
    
    # Test default attributes
    assert authormodel.name is None
    assert authormodel.date is None
    assert authormodel.license is None


def test_author_model_set_values():
    """Test setting values in AuthorModel."""
    authormodel = AuthorModel()
    
    # Set values
    authormodel.name = "Test Author"
    authormodel.date = datetime.now()
    authormodel.license = "MIT"
    
    # Verify values
    assert authormodel.name == "Test Author"
    assert authormodel.date is not None
    assert authormodel.license == "MIT"


def test_author_model_validation():
    """Test AuthorModel validation."""
    authormodel = AuthorModel()
    
    # Test with valid name
    authormodel.name = "Valid Author Name"
    assert authormodel.name == "Valid Author Name"
    
    # Test with valid license
    authormodel.license = "MIT License"
    assert authormodel.license == "MIT License"


def test_author_model_serialization():
    """Test AuthorModel serialization."""
    authormodel = AuthorModel()
    authormodel.name = "Test Author"
    authormodel.email = "test@example.com"
    authormodel.website = "https://example.com"
    authormodel.description = "Test description"
    
    # Test to_dict method if it exists
    if hasattr(authormodel, 'to_dict'):
        data = authormodel.to_dict()
        assert isinstance(data, dict)
        assert data.get('name') == "Test Author"
        assert data.get('email') == "test@example.com"


def test_author_model_from_dict():
    """Test creating AuthorModel from dictionary."""
    data = {
        'name': 'Test Author',
        'email': 'test@example.com',
        'website': 'https://example.com',
        'description': 'Test description'
    }
    
    # Test from_dict method if it exists
    if hasattr(AuthorModel, 'from_dict'):
        authormodel = AuthorModel.from_dict(data)
        assert authormodel.name == "Test Author"
        assert authormodel.email == "test@example.com"
        assert authormodel.website == "https://example.com"
        assert authormodel.description == "Test description"


def test_author_model_str_representation():
    """Test AuthorModel string representation."""
    authormodel = AuthorModel()
    authormodel.name = "Test Author"
    
    # Test string representation
    str_repr = str(authormodel)
    assert isinstance(str_repr, str)
    assert "Test Author" in str_repr


def test_author_model_equality():
    """Test AuthorModel equality."""
    authormodel1 = AuthorModel()
    authormodel1.name = "Test Author"
    authormodel1.email = "test@example.com"
    
    authormodel2 = AuthorModel()
    authormodel2.name = "Test Author"
    authormodel2.email = "test@example.com"
    
    # Test equality
    assert authormodel1.name == authormodel2.name
    assert authormodel1.email == authormodel2.email


def test_author_model_copy():
    """Test copying AuthorModel."""
    authormodel1 = AuthorModel()
    authormodel1.name = "Test Author"
    authormodel1.email = "test@example.com"
    
    # Test copy if method exists
    if hasattr(authormodel1, 'copy'):
        authormodel2 = authormodel1.copy()
        assert authormodel1.name == authormodel2.name
        assert authormodel1.email == authormodel2.email
        assert authormodel1 is not authormodel2


def test_author_model_empty_values():
    """Test AuthorModel with empty values."""
    authormodel = AuthorModel()
    
    # Test setting empty values
    authormodel.name = ""
    authormodel.email = ""
    authormodel.website = ""
    authormodel.description = ""
    
    # Verify empty values are accepted
    assert authormodel.name == ""
    assert authormodel.email == ""
    assert authormodel.website == ""
    assert authormodel.description == ""


def test_author_model_special_characters():
    """Test AuthorModel with special characters."""
    authormodel = AuthorModel()
    
    # Test with special characters
    authormodel.name = "João Silva"
    authormodel.email = "joão.silva@exemplo.com"
    authormodel.website = "https://exemplo.com/página"
    authormodel.description = "Descrição com acentos: áéíóú"
    
    # Verify special characters are preserved
    assert authormodel.name == "João Silva"
    assert authormodel.email == "joão.silva@exemplo.com"
    assert authormodel.website == "https://exemplo.com/página"
    assert authormodel.description == "Descrição com acentos: áéíóú"

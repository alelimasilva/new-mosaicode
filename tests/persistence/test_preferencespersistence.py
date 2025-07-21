# Migrated from unittest/TestBase to pytest.
import pytest
from pathlib import Path
from mosaicode.persistence.preferencespersistence import PreferencesPersistence
from mosaicode.model.preferences import Preferences

def test_load_save():
    """Test load and save preferences."""
    preferences = Preferences()
    preferences.author = "Test Author"
    preferences.license = "MIT"
    preferences.grid = 20
    preferences.width = 1000
    preferences.height = 600
    
    result = PreferencesPersistence.save(preferences, "/tmp/")
    assert result is True
    
    loaded_preferences = PreferencesPersistence.load(Path("/tmp"))
    assert loaded_preferences is not None
    assert loaded_preferences.author == "Test Author"
    assert loaded_preferences.license == "MIT"
    assert loaded_preferences.grid == 20
    assert loaded_preferences.width == 1000
    assert loaded_preferences.height == 600

def test_load_non_existent():
    """Test loading non-existent preferences file."""
    result = PreferencesPersistence.load(Path("/tmp/nonexistent"))
    assert result is not None  # Returns default preferences

def test_save_no_permission():
    """Test saving without permission."""
    preferences = Preferences()
    result = PreferencesPersistence.save(preferences, "/root/")
    assert result is False


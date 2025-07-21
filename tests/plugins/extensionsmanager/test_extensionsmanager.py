# -*- coding: utf-8 -*-
"""
Tests for ExtensionsManager class.
Migrated from unittest to pytest.
"""
import pytest
from mosaicode.plugins.extensionsmanager.extensionsmanager import ExtensionsManager


def test_extensionsmanager_load(main_window):
    """Test ExtensionsManager load functionality."""
    extensions_manager = ExtensionsManager()
    extensions_manager.load(main_window)
    
    assert extensions_manager is not None


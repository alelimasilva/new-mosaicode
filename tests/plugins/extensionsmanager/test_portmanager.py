# -*- coding: utf-8 -*-
"""
Tests for PortManager class.
Migrated from unittest to pytest.
"""
import pytest
from mosaicode.plugins.extensionsmanager.portmanager import PortManager


@pytest.fixture
def port_manager(main_window):
    """Create a test port manager."""
    return PortManager(main_window)


def test_portmanager_initialization(port_manager):
    """Test PortManager initialization."""
    assert port_manager is not None


def test_portmanager_base(main_window):
    """Test PortManager base functionality."""
    widget = PortManager(main_window)
    
    assert widget is not None


# -*- coding: utf-8 -*-
"""
Tests for PortEditor class.
Migrated from unittest to pytest.
"""
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib
import pytest
from mosaicode.system import System
from mosaicode.plugins.extensionsmanager.portmanager import PortManager
from mosaicode.plugins.extensionsmanager.porteditor import PortEditor


@pytest.fixture
def port_editor(main_window):
    """Create a test port editor."""
    port_manager = PortManager(main_window)
    return PortEditor(port_manager, None)


def test_porteditor_initialization(port_editor):
    """Test PortEditor initialization."""
    assert port_editor is not None


def test_porteditor_base(main_window):
    """Test PortEditor base functionality."""
    port_manager = PortManager(main_window)
    widget = PortEditor(port_manager, None)
    
    assert widget is not None


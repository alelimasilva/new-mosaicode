# -*- coding: utf-8 -*-
"""
Tests for BlockMenu.
Migrated from unittest to pytest.
"""
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
import pytest

from mosaicode.GUI.blockmenu import BlockMenu

@pytest.fixture
def blockmenu():
    """Create a test BlockMenu."""
    return BlockMenu()


def test_show(blockmenu):
    event = Gdk.Event().new(Gdk.EventType.BUTTON_PRESS)
    event.button = 1
    # Mock de bloco com atributo 'diagram' como widget GTK
    class DummyBlock:
        diagram = Gtk.Box()
    block = DummyBlock()
    blockmenu.show(block, event)
    blockmenu.collapse_menu_item.emit("activate")
    blockmenu.delete_menu_item.emit("activate")
    blockmenu.destroy()

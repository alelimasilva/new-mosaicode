# -*- coding: utf-8 -*-
"""
Tests for MainWindow.
Migrated from unittest to pytest.
"""
import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
import pytest

from mosaicode.GUI.mainwindow import MainWindow


@pytest.fixture
def main_window():
    """Create a test MainWindow."""
    return MainWindow()


def test_set_title(main_window):
    """Test MainWindow set_title method."""
    main_window.set_title("Test")


def test_event(main_window):
    """Test MainWindow event handling."""
    event = Gdk.Event()
    event.key.type = Gdk.EventType.KEY_PRESS
    event.state = Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD2_MASK
    event.keyval = Gdk.KEY_a
    main_window.emit("key-press-event", event)
    main_window.emit("check-resize")
    main_window.emit("delete_event", event)
    event.keyval = Gdk.KEY_b
    main_window.emit("key-press-event", event)


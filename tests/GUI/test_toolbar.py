# -*- coding: utf-8 -*-
"""
Tests for Toolbar.
Migrated from unittest to pytest.
"""
import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
import pytest

from mosaicode.GUI.toolbar import Toolbar


@pytest.fixture
def toolbar():
    """Create a test Toolbar."""
    from mosaicode.GUI.mainwindow import MainWindow
    main_window = MainWindow()
    return Toolbar(main_window)


def test_events(toolbar):
    """Test Toolbar events."""
    gdkevent = Gdk.Event()
    gdkevent.key.type = Gdk.EventType.BUTTON_PRESS
    children = toolbar.get_children()
    if children:
        button = children[0]
        button.emit("button-press-event", gdkevent)


def test_update_threads(toolbar):
    """Test Toolbar update_threads method."""
    from mosaicode.GUI.diagram import Diagram
    from mosaicode.GUI.mainwindow import MainWindow
    
    main_window = MainWindow()
    diagram = Diagram(main_window)
    
    toolbar.update_threads({"test": [diagram, None]})
    toolbar.update_threads({"test": [diagram, None]})


def test_click_button(toolbar):
    """Test Toolbar button click."""
    if hasattr(toolbar, 'actions') and toolbar.actions:
        # Get first action key and check if it's a widget
        first_key = list(toolbar.actions.keys())[0]
        action = toolbar.actions[first_key]
        if hasattr(action, 'emit'):
            action.emit("clicked")
        else:
            # If it's a function, just call it
            action()


# -*- coding: utf-8 -*-
"""
Tests for SaveFileField class.
Migrated from unittest to pytest.
"""
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
import pytest
import threading
from time import sleep
from mosaicode.GUI.fields.savefilefield import SaveFileField


@pytest.fixture
def field():
    """Create a test save file field."""
    field = SaveFileField({"label": "test", "value": "True"}, None)
    field.set_parent_window(None)
    return field


def event(widget, event):
    """Event handler for testing."""
    pass


def test_savefilefield_initialization():
    """Test SaveFileField initialization with different parameters."""
    # Test with False value
    field_false = SaveFileField({"label": "test", "value": "False"}, None)
    
    # Test with True value
    field_true = SaveFileField({"label": "test", "value": "True"}, None)
    
    # All should be created without errors
    assert field_false is not None
    assert field_true is not None


def test_savefilefield_value_operations(field):
    """Test SaveFileField value set and get operations."""
    # Test with "False" value
    value1 = "False"
    field.set_value(value1)
    value2 = field.get_value()
    assert value1 == value2, 'incorrect value'
    
    # Test with "True" value
    value1 = "True"
    field.set_value(value1)
    value2 = field.get_value()
    assert value1 == value2, 'incorrect value'


def test_savefilefield_click_ok():
    """Test SaveFileField click OK functionality."""
    field = SaveFileField({}, event)
    field.set_parent_window(Gtk.Window.new(Gtk.WindowType.TOPLEVEL))
    
    # 0 is the label, 1 is the box
    vbox = field.get_children()[1]
    # 0 is the frame, 1 is the button
    button = vbox.get_children()[1]
    
    def close_window_on_ok():
        field.dialog.set_current_folder("Test")
        field.dialog.set_current_name("Test")
        field.dialog.response(Gtk.ResponseType.OK)
        field.dialog.response(Gtk.ResponseType.ACCEPT)
        t1.join()
    
    t1 = threading.Thread(target=button.clicked)
    t1.start()
    sleep(0.5)
    close_window_on_ok()


def test_savefilefield_click_cancel():
    """Test SaveFileField click Cancel functionality."""
    field = SaveFileField({}, event)
    field.set_parent_window(Gtk.Window.new(Gtk.WindowType.TOPLEVEL))
    
    # 0 is the label, 1 is the box
    vbox = field.get_children()[1]
    # 0 is the frame, 1 is the button
    button = vbox.get_children()[1]
    
    def close_window_on_cancel():
        field.dialog.response(Gtk.ResponseType.CANCEL)
        t2.join()
    
    t2 = threading.Thread(target=button.clicked)
    t2.start()
    sleep(0.5)
    close_window_on_cancel()


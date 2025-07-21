# -*- coding: utf-8 -*-
"""
Tests for OpenFileField class.
Migrated from unittest to pytest.
"""
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
import pytest
import threading
from time import sleep
from mosaicode.GUI.fields.openfilefield import OpenFileField


@pytest.fixture
def field():
    """Create a test open file field."""
    field = OpenFileField({"label": "test", "value": "True"}, None)
    field.set_parent_window(None)
    return field


def event(widget, event):
    """Event handler for testing."""
    pass


def test_openfilefield_initialization():
    """Test OpenFileField initialization with different parameters."""
    # Test with False value
    field_false = OpenFileField({"label": "test", "value": "False"}, None)
    
    # Test with True value
    field_true = OpenFileField({"label": "test", "value": "True"}, None)
    
    # All should be created without errors
    assert field_false is not None
    assert field_true is not None


def test_openfilefield_value_operations(field):
    """Test OpenFileField value set and get operations."""
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


def test_openfilefield_click_ok():
    """Test OpenFileField click OK functionality."""
    field = OpenFileField({"value": ""}, event)
    field.set_parent_window(Gtk.Window.new(Gtk.WindowType.TOPLEVEL))
    
    # 0 is the label, 1 is the box
    vbox = field.get_children()[1]
    # 0 is the frame, 1 is the button
    button = vbox.get_children()[1]
    
    def close_window_on_ok():
        field.dialog.select_filename("LICENSE")
        field.dialog.response(Gtk.ResponseType.OK)
        t1.join()
    
    t1 = threading.Thread(target=button.clicked)
    t1.start()
    sleep(0.5)
    close_window_on_ok()


def test_openfilefield_click_cancel():
    """Test OpenFileField click Cancel functionality."""
    field = OpenFileField({"value": "."}, event)
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


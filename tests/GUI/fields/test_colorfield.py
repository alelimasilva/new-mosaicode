# Migrated from unittest/TestBase to pytest.
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
import pytest
import threading
from time import sleep
from mosaicode.GUI.fields.colorfield import ColorField

@pytest.fixture
def color_field():
    """Create a test color field."""
    field = ColorField({"label": "test", "value": "#fff"}, None)
    field.set_parent_window(Gtk.Window.new(Gtk.WindowType.TOPLEVEL))
    return field

def event(widget, event):
    """Event handler for testing."""
    pass

def test_init():
    """Test ColorField initialization."""
    field = ColorField({"label": "test", "value": "#fff"}, None)
    field = ColorField({"label": "test", "value": "#fff000"}, None)
    field = ColorField({}, event)
    assert field is not None

def test_value():
    """Test ColorField value handling."""
    field = ColorField({"value": "#fff","format": "FFF"}, None)
    value2 = field.get_value()
    assert "#fff" == value2

    field = ColorField({"value": "#fff","format": "FFFFFF"}, None)
    value1 = "#f0f0f0"
    field.set_value(value1)
    value2 = field.get_value()
    assert value1 == value2

    field = ColorField({"value": "#fff","format": "FFFFFF"}, None)
    value1 = "#000000"
    field.set_value(value1)
    value2 = field.get_value()
    assert "#000000" == value2

    field = ColorField({"value": "#fff","format": ""}, None)
    value1 = "00:00:00:00"
    field.set_value(value1)
    value2 = field.get_value()
    assert "rgb(255,255,255)" == value2

    field = ColorField({"value": "#fff","format": ""}, None)
    value1 = "00:00:00"
    field.set_value(value1)
    value2 = field.get_value()
    assert "rgb(255,255,255)" == value2


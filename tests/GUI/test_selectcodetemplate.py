# -*- coding: utf-8 -*-
"""
Tests for SelectCodeTemplate.
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

from mosaicode.GUI.selectcodetemplate import SelectCodeTemplate
from mosaicode.system import System as System


@pytest.fixture
def selectcodetemplate():
    """Create a test SelectCodeTemplate."""
    from mosaicode.GUI.mainwindow import MainWindow
    from mosaicode.model.codetemplate import CodeTemplate
    
    System()
    main_window = MainWindow()
    
    # Create a simple code template
    code_template = CodeTemplate()
    code_template.name = "Test Template"
    code_template.language = "python"
    
    template_list = [code_template]
    dialog = SelectCodeTemplate(main_window, template_list)
    
    yield dialog
    dialog.destroy()


def test_get_value(selectcodetemplate):
    """Test SelectCodeTemplate get_value method."""
    selectcodetemplate.get_value()


def test_close_window(selectcodetemplate):
    """Test SelectCodeTemplate window closing."""
    def close_window():
        event = Gdk.Event()
        event.key.type = Gdk.EventType.BUTTON_PRESS
        selectcodetemplate.emit("button-press-event", event)
        selectcodetemplate.response(Gtk.ResponseType.OK)
        selectcodetemplate.response(Gtk.ResponseType.CANCEL)
        selectcodetemplate.close()
        return False  # Stop the timeout
    
    GLib.timeout_add(100, close_window)


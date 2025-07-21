# -*- coding: utf-8 -*-
"""
Tests for SaveDialog.
Migrated from unittest to pytest.
"""
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib
from time import sleep
import threading
import pytest

from mosaicode.GUI.savedialog import SaveDialog


@pytest.fixture
def dialog():
    """Create a test SaveDialog."""
    from mosaicode.GUI.mainwindow import MainWindow
    main_window = MainWindow()
    
    # Test different constructor variations
    dialog = SaveDialog(main_window, "Test", None, "*.jpg")
    dialog = SaveDialog(main_window, "Test", "Test", None)
    
    yield dialog
    dialog.destroy()
    dialog.close()


def test_run(dialog):
    """Test SaveDialog run method."""
    t1 = threading.Thread(target=dialog.run, args=())
    t1.start()
    sleep(1)
    dialog.response(Gtk.ResponseType.OK)
    t1.join()

# -*- coding: utf-8 -*-
"""
Tests for OpenDialog.
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

from mosaicode.GUI.opendialog import OpenDialog


def test_run():
    """Test OpenDialog constructor and run."""
    from mosaicode.GUI.mainwindow import MainWindow
    main_window = MainWindow()
    
    # Test different constructor variations
    dialog = OpenDialog("Test", main_window, "*.jpg", ".")
    dialog = OpenDialog("Test", main_window, None, None)
    dialog = OpenDialog("Test", main_window, "*.mscd", None)
    
    t1 = threading.Thread(target=dialog.run, args=())
    t1.start()
    sleep(1)
    dialog.select_filename("LICENSE")
    dialog.response(Gtk.ResponseType.OK)
    t1.join()
    dialog.close()
    dialog.destroy()

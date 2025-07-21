# -*- coding: utf-8 -*-
"""
Tests for MessageDialog.
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

from mosaicode.GUI.messagedialog import MessageDialog


def test_constructor():
    """Test MessageDialog constructor and run."""
    from mosaicode.GUI.mainwindow import MainWindow
    main_window = MainWindow()
    
    dialog = MessageDialog("Test Message Dialog", "Test", main_window)
    t1 = threading.Thread(target=dialog.run, args=())
    t1.start()
    sleep(1)
    dialog.response(Gtk.ResponseType.OK)
    t1.join()
    dialog.close()
    dialog.destroy()


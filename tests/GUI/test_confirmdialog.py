# -*- coding: utf-8 -*-
"""
Tests for ConfirmDialog.
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

from mosaicode.GUI.confirmdialog import ConfirmDialog


@pytest.fixture
def dialog():
    """Create a test ConfirmDialog."""
    from mosaicode.GUI.mainwindow import MainWindow
    main_window = MainWindow()
    dialog = ConfirmDialog("Test Confirm Dialog", main_window)
    yield dialog
    dialog.destroy()


def test_run_ok(dialog):
    """Test ConfirmDialog OK response."""
    t1 = threading.Thread(target=dialog.run, args=())
    t1.start()
    sleep(1)
    dialog.response(Gtk.ResponseType.OK)
    t1.join()


def test_run_cancel(dialog):
    """Test ConfirmDialog Cancel response."""
    t1 = threading.Thread(target=dialog.run, args=())
    t1.start()
    sleep(1)
    dialog.response(Gtk.ResponseType.CANCEL)
    t1.join()

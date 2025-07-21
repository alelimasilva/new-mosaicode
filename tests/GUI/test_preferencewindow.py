# -*- coding: utf-8 -*-
"""
Tests for PreferenceWindow.
Migrated from unittest to pytest.
"""
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
from time import sleep
import threading
import pytest

from mosaicode.GUI.preferencewindow import PreferenceWindow


@pytest.fixture
def preference_window():
    """Create a test PreferenceWindow."""
    from mosaicode.GUI.mainwindow import MainWindow
    main_window = MainWindow()
    dialog = PreferenceWindow(main_window)
    
    yield dialog
    dialog.destroy()
    dialog.close()


def test_event(preference_window):
    """Test PreferenceWindow event handling."""
    t1 = threading.Thread(target=preference_window.run, args=())
    t1.start()
    sleep(1)
    preference_window.response(Gtk.ResponseType.OK)
    t1.join()

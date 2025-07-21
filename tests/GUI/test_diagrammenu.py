# -*- coding: utf-8 -*-
"""
Tests for DiagramMenu.
Migrated from unittest to pytest.
"""
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
import pytest

from mosaicode.GUI.diagrammenu import DiagramMenu
from mosaicode.GUI.diagram import Diagram

@pytest.fixture
def diagrammenu():
    return DiagramMenu()

@pytest.fixture
def diagram():
    from mosaicode.GUI.mainwindow import MainWindow
    main_window = MainWindow()
    return Diagram(main_window)

def test_show(diagrammenu, diagram):
    event = Gdk.Event().new(Gdk.EventType.BUTTON_PRESS)
    event.button = 1
    diagrammenu.show(diagram, event)
    diagrammenu.uncollapse_menu_item.emit("activate")
    diagrammenu.collapse_menu_item.emit("activate")
    diagrammenu.clear_menu_item.emit("activate")
    diagrammenu.insert_menu_item.emit("activate")
    diagrammenu.delete_menu_item.emit("activate")
    diagrammenu.destroy()

# -*- coding: utf-8 -*-
"""
Tests for Menu.
Migrated from unittest to pytest.
"""
import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
import pytest

from mosaicode.GUI.menu import Menu
from mosaicode.system import System

@pytest.fixture
def main_window():
    from mosaicode.GUI.mainwindow import MainWindow
    return MainWindow()

@pytest.fixture
def menu(main_window):
    return Menu(main_window)

def test_new(main_window):
    Menu(main_window)

def test_add_help(menu):
    menu.add_help()

def test_event(menu):
    menuitem = menu.help_menu.get_children()[0]
    menuitem.emit("activate")

def test_update_examples(menu):
    System.get_list_of_examples().append("language/framework/test")
    System.get_list_of_examples().append("language/framework/test1")
    menu.update_examples(System.get_list_of_examples())
    System.get_list_of_examples().append("test")
    menu.update_examples(System.get_list_of_examples())
    # language
    menu.example_menu.get_children()[0].activate()
    # extension
    menu.example_menu.get_children()[0].get_children()[0].activate()

def test_update_recent_files(menu):
    menu.update_recent_files(["file1", "file2"])
    menu.update_recent_files(["file1", "file2"])
    menu.update_recent_files(None)

def test_update_blocks(menu):
    menu.update_blocks(System.get_blocks())
    menu.update_blocks(System.get_blocks())

def test_menu_item(menu):
    first_key = list(menu.actions.keys())[0]
    action = menu.actions[first_key]
    if hasattr(action, 'emit'):
        action.emit("activate")
    elif callable(action):
        action()

def test_recent_files(menu):
    menu.update_recent_files(["file1", "file2"])
    menu.recent_files_menu.get_children()[0].emit("activate")

def test_key_event(menu):
    event = Gdk.Event()
    event.key.type = Gdk.EventType.KEY_PRESS
    event.state = Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD2_MASK
    event.keyval = Gdk.KEY_a
    menu.emit("key-press-event", event)
    menu.emit("check-resize")
    menu.emit("delete_event", event)
    event.keyval = Gdk.KEY_b
    menu.emit("key-press-event", event)


# -*- coding: utf-8 -*-
"""
Tests for Diagram.
Migrated from unittest to pytest.
"""
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
import pytest

from mosaicode.system import System
from mosaicode.GUI.diagram import Diagram
from mosaicode.model.port import Port

@pytest.fixture
def main_window():
    from mosaicode.GUI.mainwindow import MainWindow
    return MainWindow()

@pytest.fixture
def diagram(main_window):
    return Diagram(main_window)

@pytest.fixture
def block1(diagram):
    from mosaicode.model.blockmodel import BlockModel
    from mosaicode.GUI.block import Block
    # Cria portas válidas
    input_port = Port(conn_type="input", name="input_1", label="Input 1", index=0, type_index=0)
    output_port = Port(conn_type="output", name="output_1", label="Output 1", index=1, type_index=0)
    block_model = BlockModel()
    block_model.ports = [input_port, output_port]
    block_model.maxIO = 2
    return Block(diagram, block_model)

@pytest.fixture
def block2(diagram):
    from mosaicode.model.blockmodel import BlockModel
    from mosaicode.GUI.block import Block
    input_port = Port(conn_type="input", name="input_2", label="Input 2", index=0, type_index=0)
    output_port = Port(conn_type="output", name="output_2", label="Output 2", index=1, type_index=0)
    block_model = BlockModel()
    block_model.ports = [input_port, output_port]
    block_model.maxIO = 2
    return Block(diagram, block_model)

@pytest.fixture
def comment():
    from mosaicode.model.commentmodel import CommentModel
    return CommentModel()

@pytest.fixture(autouse=True)
def setup_diagram(main_window, diagram, block1, block2, comment):
    main_window.main_control.add_block(block1)
    main_window.main_control.add_block(block2)
    main_window.main_control.add_comment(comment)


def test_redraw(diagram):
    diagram.redraw()

def test_resize(diagram):
    diagram.resize(None)

def test_show_block_menu(diagram, block1):
    event = Gdk.Event().new(Gdk.EventType.BUTTON_PRESS)
    event.button = 3
    diagram.show_block_menu(block1, event)

def test_change_zoom(diagram):
    diagram.change_zoom(System.ZOOM_IN)
    diagram.change_zoom(System.ZOOM_OUT)
    diagram.change_zoom(System.ZOOM_ORIGINAL)

def test_show_elements(diagram, block1, comment):
    diagram.show_comment_property(comment)
    diagram.show_block_property(block1)

def test_selection(diagram):
    diagram.select_all()
    diagram.deselect_all()

def test_connection(diagram, block1, block2):
    diagram.start_connection(block1, block1.ports[0])
    diagram.end_connection(block2, block2.ports[1])

def test_button_press_event(diagram):
    event = Gdk.Event().new(Gdk.EventType.BUTTON_PRESS)
    event.button = 1
    event.state = Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.MOD2_MASK
    diagram.emit("button_press_event", event)
    event.state = Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD2_MASK
    diagram.emit("button_press_event", event)
    event.button = 2
    diagram.emit("button_press_event", event)
    event.button = 3
    diagram.emit("button_press_event", event)

def test_check_limit(diagram):
    diagram.check_limit(0, 0, 800, 600)

def test_collapse(diagram):
    diagram.collapse(True)
    diagram.collapse(False)

def test_button_release_event(diagram):
    event = Gdk.Event().new(Gdk.EventType.BUTTON_PRESS)
    event.button = 1
    event.state = Gdk.ModifierType.BUTTON1_MASK
    diagram.emit("button_press_event", event)
    diagram.emit("button_release_event", event)

def test_motion_notify_event(diagram, block1, block2):
    diagram.start_connection(block1, block1.ports[0])
    diagram.end_connection(block2, block2.ports[1])
    event = Gdk.Event().new(Gdk.EventType.BUTTON_PRESS)
    event.button = 1
    event.state = Gdk.ModifierType.BUTTON1_MASK
    diagram.emit("button_press_event", event)
    diagram.emit("motion_notify_event", event)
    diagram.emit("button_release_event", event)
    diagram.emit("motion_notify_event", event)
    diagram.start_connection(block1, block1.ports[0])
    diagram.emit("motion_notify_event", event)

def test_key_press_event(diagram):
    event = Gdk.Event()
    event.key.type = Gdk.EventType.KEY_PRESS
    event.keyval = Gdk.KEY_Up
    diagram.emit("key-press-event", event)
    event.keyval = Gdk.KEY_Down
    diagram.emit("key-press-event", event)
    event.keyval = Gdk.KEY_Left
    diagram.emit("key-press-event", event)
    event.keyval = Gdk.KEY_Right
    diagram.emit("key-press-event", event)
    event.state = Gdk.ModifierType.CONTROL_MASK
    event.keyval = Gdk.KEY_Up
    diagram.emit("key-press-event", event)
    event.keyval = Gdk.KEY_Down
    diagram.emit("key-press-event", event)
    event.keyval = Gdk.KEY_Left
    diagram.emit("key-press-event", event)
    event.keyval = Gdk.KEY_Right
    diagram.emit("key-press-event", event)
    event.state = 0
    diagram.focus = True
    event.keyval = Gdk.KEY_Delete
    diagram.emit("key-press-event", event)


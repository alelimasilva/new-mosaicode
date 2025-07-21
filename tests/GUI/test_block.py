# -*- coding: utf-8 -*-
"""
Tests for Block widget.
Migrated from unittest to pytest.
"""
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
import pytest

from mosaicode.GUI.block import Block
from mosaicode.GUI.diagram import Diagram
from mosaicode.model.port import Port

@pytest.fixture
def block_env():
    """Cria ambiente de teste com main_window, diagram e alguns blocks conectados."""
    from mosaicode.GUI.mainwindow import MainWindow
    main_window = MainWindow()
    diagram = Diagram(main_window)
    
    # Cria blocos com portas adequadas
    blocks = []
    for i in range(4):
        # Cria porta de entrada
        input_port = Port(
            conn_type="input",
            name=f"input_{i}",
            label=f"Input {i}",
            index=0,
            type_index=0
        )
        
        # Cria porta de saída
        output_port = Port(
            conn_type="output", 
            name=f"output_{i}",
            label=f"Output {i}",
            index=1,
            type_index=0
        )
        
        # Cria um BlockModel com as portas
        from mosaicode.model.blockmodel import BlockModel
        block_model = BlockModel()
        block_model.ports = [input_port, output_port]
        block_model.maxIO = 2
        
        # Cria o Block GUI com o modelo
        block = Block(diagram, block_model)
        blocks.append(block)
    
    block, block1, block2, block3 = blocks
    
    # Adiciona blocos ao diagrama
    diagram.blocks = {
        str(id(block)): block, 
        str(id(block1)): block1, 
        str(id(block2)): block2, 
        str(id(block3)): block3
    }
    
    # Simula conexões (agora com portas válidas)
    diagram.start_connection(block, block.ports[1])  # porta de saída
    diagram.end_connection(block1, block1.ports[0])  # porta de entrada
    diagram.start_connection(block2, block2.ports[1])  # porta de saída
    diagram.end_connection(block3, block3.ports[0])  # porta de entrada
    diagram.start_connection(block1, block1.ports[1])  # porta de saída
    diagram.end_connection(block3, block3.ports[0])  # porta de entrada
    
    return block, block1, block2, block3

def test_adjust_position(block_env):
    block, *_ = block_env
    block.adjust_position()

def test_set_properties(block_env):
    block, *_ = block_env
    properties = block.get_properties()
    block.set_properties(properties)

def test_get_port_pos(block_env):
    block, *_ = block_env
    block.get_port_pos(block.ports[0])

def test_update_flow(block_env):
    block, block1, block2, _ = block_env
    block.is_selected = False
    block.focus = False
    block.update_flow()
    block1.update_flow()
    block2.update_flow()
    block.is_selected = True
    block.focus = True
    block.update_flow()
    block.is_collapsed = True
    block.update_flow()

def test_port_press_event(block_env):
    block, *_ = block_env
    event = Gdk.Event().new(Gdk.EventType.BUTTON_PRESS)
    event.button = 1
    event.state = Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.MOD2_MASK
    port = block.widgets["port" + str(block.ports[0])]
    port.emit("button_press_event", port, event)
    port.emit("button_release_event", port, event)
    port = block.widgets["port" + str(block.ports[1])]
    port.emit("button_press_event", port, event)
    port.emit("button_release_event", port, event)

def test_button_press_event(block_env):
    block, *_ = block_env
    event = Gdk.Event().new(Gdk.EventType.BUTTON_PRESS)
    event.button = 1
    event.state = Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.MOD2_MASK
    block.is_selected = True
    block.emit("button_press_event", block, event)
    block.is_selected = False
    block.emit("button_press_event", block, event)
    event.state = Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD2_MASK
    block.is_selected = False
    block.emit("button_press_event", block, event)
    event.button = 3
    block.emit("button_press_event", block, event)

def test_motion_notify_event(block_env):
    block, *_ = block_env
    event = Gdk.Event().new(Gdk.EventType.BUTTON_PRESS)
    event.button = 1
    event.state = Gdk.ModifierType.BUTTON2_MASK
    block.emit("motion_notify_event", block, event)
    event.state = Gdk.ModifierType.BUTTON1_MASK
    block.emit("motion_notify_event", block, event)
    event.state = Gdk.ModifierType.BUTTON1_MASK
    block.diagram.curr_connector = block
    block.emit("motion_notify_event", block, event)

def test_enter_leave_event(block_env):
    block, *_ = block_env
    event = Gdk.Event().new(Gdk.EventType.BUTTON_PRESS)
    event.button = 1
    event.state = Gdk.ModifierType.BUTTON1_MASK
    block.emit("enter_notify_event", block, event)
    block.emit("leave_notify_event", block, event)


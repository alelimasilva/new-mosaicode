# -*- coding: utf-8 -*-
"""
Tests for Connector widget.
Migrated from unittest to pytest.
"""
import gi
gi.require_version('Gdk', '3.0')
gi.require_version('GooCanvas', '2.0')
from gi.repository import GooCanvas
from gi.repository import Gdk
import pytest

from mosaicode.GUI.connector import Connector
from mosaicode.GUI.block import Block
from mosaicode.model.port import Port
from mosaicode.system import System


@pytest.fixture
def connector():
    """Create a test Connector."""
    from mosaicode.GUI.mainwindow import MainWindow
    from mosaicode.GUI.diagram import Diagram
    from mosaicode.model.blockmodel import BlockModel
    
    main_window = MainWindow()
    diagram = Diagram(main_window)
    
    # Create source block
    source_block_model = BlockModel()
    source_block = Block(diagram, source_block_model)
    
    # Create port
    port = Port()
    source_block.ports.append(port)
    
    return Connector(diagram, source_block, port)


def test_update_flow(connector):
    """Test Connector update_flow method."""
    connector.input = None
    connector.update_flow()
    point = (0, 0)
    connector.update_flow(point)
    
    # Create input block
    from mosaicode.GUI.mainwindow import MainWindow
    from mosaicode.GUI.diagram import Diagram
    from mosaicode.model.blockmodel import BlockModel
    
    main_window = MainWindow()
    diagram = Diagram(main_window)
    input_block_model = BlockModel()
    connector.input = Block(diagram, input_block_model)
    connector.input.move(100, 100)
    connector.input_port = Port()
    
    # Test different connection types
    System.get_preferences().connection = "Curve"
    connector.update_flow()
    System.get_preferences().connection = "Line"
    connector.update_flow()
    System.get_preferences().connection = "Square"
    connector.update_flow()


def test_events(connector):
    """Test Connector events."""
    gdkevent = Gdk.Event()
    gdkevent.key.type = Gdk.EventType.MOTION_NOTIFY

    connector.emit("enter-notify-event", connector, gdkevent)
    connector.is_selected = True
    connector.emit("leave-notify-event", connector, gdkevent)

    connector.is_selected = False
    gdkevent.key.type = Gdk.EventType.DOUBLE_BUTTON_PRESS
    connector.emit("button-press-event", connector, gdkevent)
    gdkevent.button = 3
    connector.emit("button-press-event", connector, gdkevent)
    connector.is_selected = True
    connector.emit("button-press-event", connector, gdkevent)


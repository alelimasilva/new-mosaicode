import pytest
import gi
import os
import shutil
import tempfile
from pathlib import Path
from time import sleep

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk

from mosaicode.GUI.block import Block
from mosaicode.GUI.comment import Comment
from mosaicode.GUI.diagram import Diagram
from mosaicode.GUI.mainwindow import MainWindow
from mosaicode.GUI.fieldtypes import *
from mosaicode.model.blockmodel import BlockModel
from mosaicode.model.port import Port
from mosaicode.model.codetemplate import CodeTemplate
from mosaicode.model.connectionmodel import ConnectionModel
from mosaicode.control.diagramcontrol import DiagramControl
from mosaicode.control.blockcontrol import BlockControl
from mosaicode.system import System
from mosaicode.utils.pydantic_schemas import BlockDefaultValues, PortDefaultValues

@pytest.fixture
def temp_test_dir():
    test_dir = Path(tempfile.mkdtemp(prefix="mosaicode_test_"))
    System()
    System.reload()
    yield test_dir
    if test_dir.exists():
        shutil.rmtree(test_dir)

@pytest.fixture
def main_window():
    return MainWindow()

@pytest.fixture
def diagram(main_window):
    d = Diagram(main_window)
    d.language = "Test"
    d.zoom = 2
    d.code_template = create_code_template()
    return d

@pytest.fixture
def diagram_control(diagram):
    dc = DiagramControl(diagram)
    dc.connectors = []
    dc.language = "language"
    return dc

@pytest.fixture
def block(diagram_control):
    block_model = BlockModel()
    port0 = Port()
    port0.label = "Test0"
    port0.conn_type = Port.OUTPUT
    port0.name = "Test0"
    port0.type = "Test"
    port0.index = 0
    port1 = Port()
    port1.label = "Test1"
    port1.conn_type = Port.INPUT
    port1.name = "Test1"
    port1.type = "Test"
    port1.index = 1
    block_model.ports = [port0, port1]
    block_model.help = "Test"
    block_model.label = "Test"
    block_model.color = "#C8C819"
    block_model.group = "Test"
    block_model.codes = {"code0": "Test", "Code1": "Test", "Code2": "Test"}
    block_model.type = "Test"
    block_model.language = "Test"
    block_model.properties = [{"name": "test", "label": "Test", "value": "0", "type": MOSAICODE_FLOAT}]
    block_model.extension = "Test"
    block_model.file = None
    block_model.id = len(System.get_blocks()) + 1
    block = Block(diagram_control.diagram, block_model)
    System.get_blocks()[block.type] = block
    from mosaicode.persistence.blockpersistence import BlockPersistence
    temp_dir = "mosaicode/extensions/blocks"
    os.makedirs(temp_dir, exist_ok=True)
    BlockPersistence.save(block, temp_dir)
    from mosaicode.system import System as MosaicodeSystem
    MosaicodeSystem.reload()
    return block

def create_code_template():
    code_template = CodeTemplate()
    code_template.name = "TestTemplate"
    code_template.language = "Test"
    code_template.codes = {"main": "print('Hello World')"}
    code_template.code_parts = ["main"]
    code_template.command = "python $dir_name$index.py"
    code_template.description = "Test template"
    code_template.properties = []
    return code_template

def refresh_gui(delay=0):
    while Gtk.events_pending():
        Gtk.main_iteration_do(False)
    sleep(delay)

def create_comment(diagram):
    return Comment(diagram, None)

def create_port():
    port = Port()
    port.label = "TestPort"
    port.conn_type = Port.OUTPUT
    port.name = "TestPort"
    port.type = "Test"
    port.index = 0
    return port 
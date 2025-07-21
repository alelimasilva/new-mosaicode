# -*- coding: utf-8 -*-
"""
Base test class for mosaicode tests.
Updated for new architecture with Pydantic models and JSON configuration.
"""
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib
import unittest
from time import sleep
from abc import ABCMeta
from pathlib import Path
from typing import Dict, List, Optional, Any
import tempfile
import shutil
import json

# Mosaicode imports
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


class TestBase(unittest.TestCase):
    """Base test class with updated helpers for new mosaicode architecture."""
    __metaclass__ = ABCMeta

    def setUp(self):
        """Set up test environment."""
        # Create temporary test directory
        self.test_dir = Path(tempfile.mkdtemp(prefix="mosaicode_test_"))
        
        # Initialize system for testing
        System()
        System.reload()

    def tearDown(self):
        """Clean up test environment."""
        # Remove temporary test directory
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def refresh_gui(self, delay=0):
        """Process GTK events and optionally wait."""
        while Gtk.events_pending():
            Gtk.main_iteration_do(False)
        sleep(delay)

    def create_main_window(self):
        """Create a main window for testing."""
        return MainWindow()

    def create_diagram(self, main_window=None):
        """Create a test diagram."""
        if main_window is None:
            main_window = self.create_main_window()
        diagram = Diagram(main_window)
        diagram.language = "Test"
        diagram.zoom = 2
        diagram.code_template = self.create_code_template()
        return diagram

    def create_full_diagram(self):
        """Create a complete diagram with blocks and connections."""
        main_window = self.create_main_window()
        diagram = Diagram(main_window)
        diagram_control = self.create_diagram_control()
        diagram = diagram_control.diagram

        block1 = self.create_block()
        print(f"[DEBUG] Adicionando block1 ao diagrama: valor={block1}, tipo={type(block1)}")
        diagram_control.add_block(block1)

        block2 = self.create_block()
        print(f"[DEBUG] Adicionando block2 ao diagrama: valor={block2}, tipo={type(block2)}")
        diagram_control.add_block(block2)

        # Ensure blocks have enough ports before creating connections
        if len(block1.ports) >= 2 and len(block2.ports) >= 2:
            connection = ConnectionModel(
                        diagram,
                        block1,
                        block1.ports[0],
                        block2,
                        block2.ports[1]
                        )
            diagram_control.add_connection(connection)

            connection = ConnectionModel(
                        diagram,
                        block1,
                        block1.ports[1],
                        block2,
                        block2.ports[0]
                        )
            diagram_control.add_connection(connection)

        # Removed problematic connection with None values

        comment = self.create_comment()
        main_window.main_control.add_comment(comment)
        diagram_control.add_comment(comment)
        return diagram

    def create_diagram_control(self, diagram=None):
        """Create a diagram control for testing."""
        if diagram is None:
            diagram = self.create_diagram()
        diagram_control = DiagramControl(diagram)
        diagram_control.connectors = []
        diagram_control.language = "language"
        return diagram_control

    def create_block(self, diagram_control=None):
        """Create a test block with updated structure."""
        if diagram_control is None:
            diagram_control = self.create_diagram_control()

        block_model = BlockModel()

        # Create ports using new structure
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

        # Set block properties using new structure
        block_model.help = "Test"
        block_model.label = "Test"
        block_model.color = "#C8C819"  # Updated color format
        block_model.group = "Test"
        block_model.codes = {"code0":"Test",
                       "Code1":"Test",
                       "Code2":"Test"}
        block_model.type = "Test"
        block_model.language = "Test"
        block_model.properties = [{"name": "test",
                             "label": "Test",
                             "value": "0",
                             "type": MOSAICODE_FLOAT
                             }]
        block_model.extension = "Test"
        block_model.file = None
        block_model.id = len(System.get_blocks()) + 1  # Add unique ID
        
        block = Block(diagram_control.diagram, block_model)
        # Don't override block.id - let the Block constructor handle it
        # Register the block in System.get_blocks() for persistence to work correctly
        System.get_blocks()[block.type] = block
        # Salva o bloco como extensão temporária reconhecida pelo mosaicode
        from mosaicode.persistence.blockpersistence import BlockPersistence
        import os
        temp_dir = "mosaicode/extensions/blocks"
        os.makedirs(temp_dir, exist_ok=True)
        BlockPersistence.save(block, temp_dir)
        from mosaicode.system import System as MosaicodeSystem
        MosaicodeSystem.reload()
        # DEBUG: Verificar tipo do bloco criado
        print(f"[DEBUG] Bloco criado em create_block: valor={block}, tipo={type(block)}")
        assert not isinstance(block, int), f"[ERRO] create_block retornou um inteiro: {block}"
        return block

    def create_comment(self):
        """Create a test comment."""
        comment = Comment(self.create_diagram(), None)
        return comment

    def create_port(self):
        """Create a test port."""
        port = Port()
        return port

    def create_connection(self):
        """Create a test connection."""
        from mosaicode.model.connectionmodel import ConnectionModel
        connection = ConnectionModel(
            self.create_diagram(),
            self.create_block(),
            self.create_port(),
            self.create_block(),
            self.create_port()
        )
        return connection

    def create_code_template(self):
        """Create a test code template with updated structure."""
        code_template = CodeTemplate()
        code_template.name = "webaudio"
        code_template.type = "Test"
        code_template.language = "javascript"
        code_template.command = "python -m webbrowser -t $dir_name$index.html\n"
        code_template.description = "Javascript / webaudio code template"

        code_template.code_parts = ["onload", "function", "declaration", "execution", "html"]
        code_template.properties = [{"name": "title",
                            "label": "Title",
                            "value": "Title",
                            "type": MOSAICODE_STRING
                            }
                           ]

        # Add code templates to the codes dictionary
        code_template.codes["html"] = r"""
<html>
    <head>
        <meta http-equiv="Cache-Control" content="no-store" />
        <!-- $author$ $license$ -->
        <title>$prop[title]$</title>
        <link rel="stylesheet" type="text/css" href="theme.css">
        <script src="functions.js"></script>
        <script>
        $single_code[function]$
        function loadme(){
        $single_code[onload]$
        return;
        }
        var context = new (window.AudioContext || window.webkitAudioContext)();
        //declaration block
        $code[declaration]$

        //execution
        $code[execution]$

        //connections
        $connections$
        </script>
    </head>

    <body onload='loadme();'>
        $code[html]$
    </body>
</html>
"""

        code_template.codes["css"] = r"""
/*
Developed by: $author$
*/
html, body {
  background: #ffeead;
  color: #ff6f69;
}
h1, p {
  color: #ff6f69;
}
#navbar a {
  color: #ff6f69;
}
.item {
  background: #ffcc5c;
}
button {
  background: #ff6f69;
  color: #ffcc5c;
}
"""

        code_template.codes["js"] = r"""
/*
Developed by: $author$
*/
$single_code[function]$
"""
        System.get_code_templates()[code_template.type] = code_template
        return code_template

    def create_test_json_file(self, data: Dict[str, Any], filename: str) -> Path:
        """Create a temporary JSON file for testing."""
        file_path = self.test_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return file_path

    def create_test_block_json(self) -> Dict[str, Any]:
        """Create test block data in JSON format."""
        return {
            "id": -1,
            "version": "0.0.1",
            "x": 0,
            "y": 0,
            "is_collapsed": False,
            "type": "TestBlock",
            "language": "javascript",
            "extension": "test",
            "file": None,
            "help": "Test block for unit testing",
            "label": "TestBlock",
            "color": "#C8C819",
            "group": "Test",
            "ports": [
                {
                    "type": "Test",
                    "label": "Output",
                    "conn_type": "OUTPUT",
                    "name": "output",
                    "index": 0
                },
                {
                    "type": "Test", 
                    "label": "Input",
                    "conn_type": "INPUT",
                    "name": "input",
                    "index": 1
                }
            ],
            "maxIO": 2,
            "properties": [
                {
                    "name": "test_prop",
                    "label": "Test Property",
                    "value": "0",
                    "type": "float"
                }
            ],
            "codes": {
                "code0": "// Test code",
                "code1": "// Another test code"
            },
            "gen_codes": {},
            "weight": 0,
            "connections": []
        }

    def create_test_port_json(self) -> Dict[str, Any]:
        """Create test port data in JSON format."""
        return {
            "version": "0.0.1",
            "type": "TestPort",
            "language": "javascript",
            "hint": "Test port hint",
            "color": "#0000FF",
            "multiple": False,
            "code": "// Port code",
            "var_name": "$block[label]$_$block[id]$_$port[name]$",
            "conn_type": "INPUT",
            "name": "test_port",
            "label": "Test Port",
            "index": 0,
            "type_index": 0,
            "file": None
        }

    def assert_valid_block_model(self, block: BlockModel):
        """Assert that a block model is valid according to new structure."""
        self.assertIsInstance(block, BlockModel)
        self.assertIsNotNone(block.type)
        self.assertIsNotNone(block.label)
        self.assertIsInstance(block.ports, list)
        self.assertIsInstance(block.properties, list)
        self.assertIsInstance(block.codes, dict)

    def assert_valid_port_model(self, port: Port):
        """Assert that a port model is valid according to new structure."""
        self.assertIsInstance(port, Port)
        self.assertIsNotNone(port.type)
        self.assertIsNotNone(port.name)
        self.assertIn(port.conn_type, [Port.INPUT, Port.OUTPUT])

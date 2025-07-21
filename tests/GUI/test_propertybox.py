# -*- coding: utf-8 -*-
"""
Tests for PropertyBox.
Migrated from unittest to pytest.
"""
import pytest

from mosaicode.GUI.fieldtypes import *
from mosaicode.GUI.propertybox import PropertyBox
from mosaicode.GUI.block import Block


@pytest.fixture
def propertybox():
    """Create a test PropertyBox."""
    from mosaicode.GUI.mainwindow import MainWindow
    main_window = MainWindow()
    return PropertyBox(main_window)


@pytest.fixture
def block():
    """Create a test Block."""
    from mosaicode.GUI.mainwindow import MainWindow
    from mosaicode.GUI.diagram import Diagram
    from mosaicode.model.blockmodel import BlockModel
    
    main_window = MainWindow()
    diagram = Diagram(main_window)
    block_model = BlockModel()
    return Block(diagram, block_model)


@pytest.fixture
def comment():
    """Create a test Comment."""
    from mosaicode.model.commentmodel import CommentModel
    return CommentModel()


@pytest.fixture
def diagram():
    """Create a test Diagram."""
    from mosaicode.GUI.mainwindow import MainWindow
    from mosaicode.GUI.diagram import Diagram
    
    main_window = MainWindow()
    return Diagram(main_window)


@pytest.fixture
def code_template():
    """Create a test CodeTemplate."""
    from mosaicode.model.codetemplate import CodeTemplate
    return CodeTemplate()


def test_set_block(propertybox, block):
    """Test PropertyBox set_block method."""
    block.properties = [{"name": "curve",
                        "label": "Curve",
                        "type": MOSAICODE_FLOAT,
                        "value": 800
                        }
                       ]
    propertybox.set_block(block)
    block.properties = [{"name": "curve",
                        "label": "Curve",
                        "type": MOSAICODE_OPEN_FILE,
                        "value": "800"
                        }
                       ]
    propertybox.set_block(block)
    propertybox.notify_block()


def test_set_comment(propertybox, comment):
    """Test PropertyBox set_comment method."""
    propertybox.set_comment(comment)
    comment.properties = []
    propertybox.set_comment(comment)
    propertybox.notify_comment()


def test_set_diagram(propertybox, diagram, code_template):
    """Test PropertyBox set_diagram method."""
    diagram.code_template = None
    propertybox.set_diagram(diagram)
    diagram.code_template = code_template
    propertybox.set_diagram(diagram)
    propertybox.notify_diagram()


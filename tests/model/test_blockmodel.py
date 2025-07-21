# -*- coding: utf-8 -*-
"""
Tests for BlockModel class.
Migrated from unittest/TestBase to pytest.
"""
import pytest
from mosaicode.model.blockmodel import BlockModel
from mosaicode.GUI.fieldtypes import *

@pytest.fixture
def block():
    return BlockModel()

def test_blockmodel_color(block):
    block.color = "#000000000000"
    assert block.get_color() == "#000000000000"
    block.color = "0"
    assert block.get_color() == "0"

def test_blockmodel_colorrgba(block):
    block.color = "#200:200:150:20"
    assert block.get_color_as_rgba() == "#200:200:150:20"
    block.color = "200:200:150:20"
    assert block.get_color_as_rgba() == "rgba(200,200,150,20)"

def test_blockmodel_properties(block):
    block.properties = [
        {"name": "time", "label": "Time", "lower": 0, "upper": 10000, "step": 1, "value": 1},
        {"name": "color", "label": "Color", "value": "#F00", "format": "FF00FF", "type": MOSAICODE_COLOR}
    ]
    erro = {"color": "time"}
    block.set_properties(erro)

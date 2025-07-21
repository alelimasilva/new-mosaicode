# -*- coding: utf-8 -*-
"""
Tests for BlockNotebook.
Migrated from unittest to pytest.
"""
import pytest
from mosaicode.system import System as System
from mosaicode.GUI.blocknotebook import BlockNotebook

@pytest.fixture
def block_notebook():
    from mosaicode.GUI.mainwindow import MainWindow
    main_window = MainWindow()
    notebook = BlockNotebook(main_window)
    blocks = System.get_blocks()
    notebook.update_blocks(blocks)
    return notebook

def test_update_blocks(block_notebook):
    blocks = System.get_blocks()
    assert block_notebook.update_blocks(blocks) is None, "Failed to update blocks"
    assert block_notebook.update_blocks(blocks) is None, "Failed to update blocks"

def test_search(block_notebook):
    query = "Add Float"
    assert block_notebook.search(query) is None

def test_get_selected_block(block_notebook):
    block_notebook.get_selected_block()
    block_notebook.set_current_page(0)
    while block_notebook.get_n_pages() > 0:
        block_notebook.remove_page(0)
        block_notebook.tabs.pop()
    block_notebook.get_selected_block()


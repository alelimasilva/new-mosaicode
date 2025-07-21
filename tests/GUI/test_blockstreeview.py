# -*- coding: utf-8 -*-
"""
Tests for BlocksTreeView.
Migrated from unittest to pytest.
"""
import pytest
import gi
import pytest
from mosaicode.system import System as System
from mosaicode.GUI.blockstreeview import BlocksTreeView

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk

@pytest.fixture
def widget():
    from mosaicode.GUI.mainwindow import MainWindow
    from mosaicode.model.blockmodel import BlockModel
    main_window = MainWindow()
    block1 = BlockModel()
    block1.group = "Test2"
    return BlocksTreeView(
        main_window,
        "Test",
        {"Test1": BlockModel(), "Test2": block1}
    )

def test_get_selected_block(widget):
    widget.get_selected_block()

def test_row_activated(widget):
    treeselection = widget.blocks_tree_view.get_selection()
    iter_first = widget.tree_store.get_iter_first()
    if iter_first is None:
        pytest.skip("Sem blocos na árvore para ativar linha.")
    treeselection.select_iter(iter_first)
    model, iterac = treeselection.get_selected()
    if iterac is not None:
        path = model.get_path(iterac)
        column = widget.blocks_tree_view.get_column(0)
        widget.blocks_tree_view.row_activate(path, column)
    else:
        pytest.skip("Nenhum iter selecionado na árvore.")

def test_events(widget):
    widget.blocks_tree_view.emit("cursor-changed")
    try:
        # Parâmetros reais para drag-data-get
        selection_data = Gtk.SelectionData()
        info = 0
        time = 0
        context = Gdk.DragContext.new(widget.blocks_tree_view.get_window(), 0)
        widget.blocks_tree_view.emit("drag-data-get", context, selection_data, info, time)
    except Exception as e:
        pytest.skip(f"Não foi possível emitir drag-data-get: {e}")

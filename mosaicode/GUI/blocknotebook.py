#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains the BlockNotebook class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from mosaicode.GUI.blockstreeview import BlocksTreeView
from typing import Any, Dict, List, Optional, Union


class BlockNotebook(Gtk.Notebook):

    """
    This class contains methods related the BlockNotebook class.
    """

    # ----------------------------------------------------------------------
    def __init__(self, main_window) -> None:
        """
        This method is the constructor.

            Parameters:
                * **main_window** (:class:`MainWindow<mosaicode.GUI.mainwindow>`)
        """
        Gtk.Notebook.__init__(self)
        self.tabs: List[Any] = []
        self.main_window = main_window
        self.set_scrollable(True)

    # ----------------------------------------------------------------------
    def update_blocks(self, blocks) -> None:
        """
        This methods update all blocks loaded for each library.

            :param blocks: blocks to update
            :return: None
        """
        languages = []

        while self.get_n_pages() > 0:
            self.remove_page(0)
            self.tabs.pop()

        for x in blocks:
            instance = blocks[x]
            name = instance.language
            name += "/" + instance.extension
            if name in languages:
                continue
            languages.append(name)

        for language in languages:
            treeview = BlocksTreeView(self.main_window, language, blocks)
            self.append_page(treeview, Gtk.Label.new(language))
            self.tabs.append(treeview)
        self.show_all()

    # ----------------------------------------------------------------------
    def search(self, query) -> None:
        """
        This method search for a block.

            Returns:
                * **Types** (:class:`list<list>`)
        """
        for blocks_tree_view in self.tabs:
            blocks_tree_view.search(query)

    # ----------------------------------------------------------------------
    def get_selected_block(self) -> Any:
        """
        This methods obtain the selected block in current tab.
            :return: selected block.
        """
        current_tab = None
        if self.get_current_page() > -1:
            current_tab = self.get_nth_page(self.get_current_page())
        if current_tab is None:
            return None
        return current_tab.get_selected_block()
# ----------------------------------------------------------------------

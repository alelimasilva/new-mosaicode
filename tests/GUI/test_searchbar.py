# -*- coding: utf-8 -*-
"""
Tests for SearchBar.
Migrated from unittest to pytest.
"""
import pytest

from mosaicode.GUI.searchbar import SearchBar


@pytest.fixture
def searchbar():
    """Create a test SearchBar."""
    from mosaicode.GUI.mainwindow import MainWindow
    main_window = MainWindow()
    return SearchBar(main_window)


def test_search_changed(searchbar):
    """Test SearchBar search_changed method."""
    searchbar.search_changed(None)


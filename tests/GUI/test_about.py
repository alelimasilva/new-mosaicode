# -*- coding: utf-8 -*-
"""
Tests for About dialog.
Migrated from unittest to pytest.
"""
import pytest

from mosaicode.GUI.about import About


@pytest.fixture
def about():
    """Create a test About dialog."""
    from mosaicode.GUI.mainwindow import MainWindow
    main_window = MainWindow()
    about = About(main_window)
    yield about
    about.destroy()


def test_get_default_size(about):
    """Test About dialog default size."""
    assert about.get_default_size() == (650, 480), "incorrect size"


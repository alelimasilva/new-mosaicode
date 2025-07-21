# -*- coding: utf-8 -*-
"""
Tests for CodeWindow.
Migrated from unittest to pytest.
"""
import pytest

from mosaicode.GUI.codewindow import CodeWindow


@pytest.fixture
def code_window():
    """Create a test CodeWindow."""
    from mosaicode.GUI.mainwindow import MainWindow
    main_window = MainWindow()
    codes = {'color': 'blue', 'fruit': 'apple', 'pet': 'dog'}
    window = CodeWindow(main_window, codes)
    yield window
    window.close()
    window.destroy()


def test_init(code_window):
    """Test CodeWindow initialization and button events."""
    code_window.save_button.emit("clicked")
    code_window.run_button.emit("clicked")

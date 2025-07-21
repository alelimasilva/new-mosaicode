# -*- coding: utf-8 -*-
"""
Tests for Status bar.
Migrated from unittest to pytest.
"""
import pytest

from mosaicode.GUI.status import Status


@pytest.fixture
def status():
    """Create a test Status bar."""
    from mosaicode.GUI.mainwindow import MainWindow
    main_window = MainWindow()
    return Status(main_window)


def test_clear(status):
    """Test Status clear method."""
    assert status.clear() is None


def test_append_text(status):
    """Test Status append_text method."""
    assert status.append_text("test_append_text") is None


def test_log(status):
    """Test Status log method."""
    assert status.log("test_append_text") is None


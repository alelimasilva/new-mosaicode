# -*- coding: utf-8 -*-
"""
Tests for ButtonBar.
Migrated from unittest to pytest.
"""
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
import pytest

from mosaicode.GUI.buttonbar import ButtonBar


@pytest.fixture
def buttonbar():
    """Create a test ButtonBar."""
    return ButtonBar()


def test_add_button(buttonbar):
    """Test ButtonBar add_button method."""
    def test_action():
        pass
    
    buttonbar.add_button({
        "icone": "document-new",  # Usar nome de ícone válido
        "action": test_action,
        "data": None
    })

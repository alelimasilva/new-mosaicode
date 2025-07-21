import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository import GObject

import pytest
from mosaicode.GUI.treeview import TreeView


@pytest.fixture
def treeview():
    """Create test treeview."""
    def action():
        pass
    
    return TreeView("Title", action, None)


def test_populate(treeview):
    """Test treeview populate method."""
    items = ["A", "B", "C"]
    treeview.populate(items)


def test_get_selection(treeview):
    """Test treeview get_selection method."""
    treeview.get_selection()

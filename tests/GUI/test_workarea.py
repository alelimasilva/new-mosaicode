import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository import GObject
from gi.repository import GLib
from time import sleep
import threading
import pytest
from mosaicode.GUI.workarea import WorkArea


@pytest.fixture
def workarea(main_window):
    """Create test workarea."""
    workarea = WorkArea(main_window)
    yield workarea
    workarea.destroy()


def test_add_diagram(workarea, diagram):
    """Test workarea add_diagram method."""
    workarea.add_diagram(diagram)


def test_rename_diagram(workarea, diagram):
    """Test workarea rename_diagram method."""
    workarea.add_diagram(diagram)
    diagram.set_modified(True)
    workarea.rename_diagram(diagram)


def test_get_diagrams(workarea):
    """Test workarea get_diagrams method."""
    workarea.get_diagrams()


def test_resize(workarea, diagram):
    """Test workarea resize method."""
    workarea.add_diagram(diagram)
    workarea.resize(None)


def test_close_tab(workarea, diagram):
    """Test workarea close_tab method."""
    workarea.add_diagram(diagram)
    workarea.close_tab(1000)


def test_close_tabs(workarea, diagram):
    """Test workarea close_tabs method."""
    workarea.add_diagram(diagram)
    diagram.set_modified(True)
    
    # Test close_tabs
    t1 = threading.Thread(target=workarea.close_tabs, args=())
    t1.start()
    sleep(1)
    workarea.confirm.response(Gtk.ResponseType.CANCEL)
    t1.join()

    # Test close_tab
    t1 = threading.Thread(target=workarea.close_tab, args=())
    t1.start()
    sleep(1)
    workarea.confirm.response(Gtk.ResponseType.CANCEL)
    t1.join()

    # Test close_tab with invalid index
    t1 = threading.Thread(target=workarea.close_tab, args=(-2,))
    t1.start()
    sleep(1)
    workarea.confirm.response(Gtk.ResponseType.CANCEL)
    t1.join()


def test_get_current_diagram(workarea, diagram):
    """Test workarea get_current_diagram method."""
    workarea.add_diagram(diagram)
    workarea.get_current_diagram()
    workarea.close_tabs()
    workarea.get_current_diagram()


def test_events(workarea, diagram):
    """Test workarea events."""
    gdkevent = Gdk.Event()
    gdkevent.key.type = Gdk.EventType.BUTTON_PRESS
    workarea.add_diagram(diagram)
    tab = workarea.get_nth_page(workarea.get_current_page())
    hbox = workarea.get_tab_label(tab)
    label = hbox.get_children()[0]
    button = hbox.get_children()[1]
    button.emit("clicked")


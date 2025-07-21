# -*- coding: utf-8 -*-
"""
Tests for Comment widget.
Migrated from unittest to pytest.
"""
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository import GObject
import pytest

from mosaicode.GUI.comment import Comment
from mosaicode.model.commentmodel import CommentModel


@pytest.fixture
def comment():
    """Create a test Comment widget."""
    from mosaicode.GUI.mainwindow import MainWindow
    from mosaicode.GUI.diagram import Diagram
    main_window = MainWindow()
    diagram = Diagram(main_window)
    comment_model = CommentModel(id=1)
    return Comment(diagram, comment_model)


def test_move(comment):
    """Test Comment move method."""
    comment.move(10, 10)


def test_set_properties(comment):
    """Test Comment set_properties method."""
    comment.set_properties(None)


def test_get_properties(comment):
    """Test Comment get_properties method."""
    comment.get_properties()


def test_adjust_position(comment):
    """Test Comment adjust_position method."""
    comment.adjust_position()


def test_update_flow(comment):
    """Test Comment update_flow method."""
    comment.is_selected = False
    comment.focus = False
    comment.update_flow()
    comment.is_selected = True
    comment.focus = True
    comment.update_flow()


def test_button_press_event(comment):
    """Test Comment button_press_event."""
    event = Gdk.Event().new(Gdk.EventType.BUTTON_PRESS)
    event.button = 1
    event.state = Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.MOD2_MASK
    comment.is_selected = True
    comment.emit("button_press_event", comment, event)
    comment.is_selected = False
    comment.emit("button_press_event", comment, event)
    event.state = Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD2_MASK
    comment.is_selected = False
    comment.emit("button_press_event", comment, event)


def test_motion_notify_event(comment):
    """Test Comment motion_notify_event."""
    event = Gdk.Event().new(Gdk.EventType.BUTTON_PRESS)
    event.button = 1
    event.state = Gdk.ModifierType.BUTTON1_MASK
    comment.emit("motion_notify_event", comment, event)
    event.state = Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.MOD2_MASK
    comment.emit("motion_notify_event", comment, event)


def test_enter_leave_event(comment):
    """Test Comment enter/leave events."""
    event = Gdk.Event().new(Gdk.EventType.BUTTON_PRESS)
    event.button = 1
    event.state = Gdk.ModifierType.BUTTON1_MASK
    comment.emit("enter_notify_event", comment, event)
    comment.emit("leave_notify_event", comment, event)


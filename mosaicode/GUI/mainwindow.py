#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains the MainWindow class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk, Gtk  # type: ignore
import os
from typing import Any, Optional, Dict, List

from mosaicode.system import System as System
from mosaicode.control.maincontrol import MainControl
from mosaicode.GUI.blockmenu import BlockMenu
from mosaicode.GUI.diagrammenu import DiagramMenu
from mosaicode.GUI.blocknotebook import BlockNotebook
from mosaicode.GUI.menu import Menu
from mosaicode.GUI.propertybox import PropertyBox
from mosaicode.GUI.searchbar import SearchBar
from mosaicode.GUI.status import Status
from mosaicode.GUI.toolbar import Toolbar
from mosaicode.GUI.workarea import WorkArea


class MainWindow(Gtk.Window):
    """
    This class contains methods related the MainWindow class.
    """

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        """
        This method is constructor.
        """
        System()
        Gtk.Window.__init__(self, title="Mosaicode")
        self.resize(
            System.get_preferences().width,
            System.get_preferences().height)
        
        # Type hints for main components
        self.main_control: MainControl = MainControl(self)
        
        # GUI components with type hints
        self.menu: Menu = Menu(self)
        self.toolbar: Toolbar = Toolbar(self)
        self.search: SearchBar = SearchBar(self)
        self.block_notebook: BlockNotebook = BlockNotebook(self)
        self.property_box: PropertyBox = PropertyBox(self)
        self.work_area: WorkArea = WorkArea(self)
        self.status: Status = Status(self)
        self.diagram_menu: DiagramMenu = DiagramMenu()
        self.menu.add_help()
        self.block_menu: BlockMenu = BlockMenu()

        System.set_log(self.status)

        # vbox main
        # -----------------------------------------------------
        # | Menu
        # -----------------------------------------------------
        # | Toolbar
        # -----------------------------------------------------
        # | V Paned bottom
        # -----------------------------------------------------

        # First Vertical Box
        vbox_main: Gtk.VBox = Gtk.VBox()
        self.add(vbox_main)
        vbox_main.pack_start(self.menu, False, True, 0)
        vbox_main.pack_start(self.toolbar, False, False, 0)
        self.vpaned_bottom: Gtk.Paned = Gtk.Paned.new(Gtk.Orientation.VERTICAL)
        vbox_main.add(self.vpaned_bottom)

        # vpaned_bottom
        # -----------------------------------------------------
        # | hpaned_work_area
        # =====================================================
        # | status
        # -----------------------------------------------------

        self.hpaned_work_area: Gtk.HPaned = Gtk.HPaned()
        self.hpaned_work_area.connect("accept-position", self.__resize)
        self.hpaned_work_area.set_position(
            System.get_preferences().hpaned_work_area)

        self.vpaned_bottom.add1(self.hpaned_work_area)
        self.vpaned_bottom.add2(self.__create_frame(self.status))
        self.vpaned_bottom.set_position(System.get_preferences().vpaned_bottom)
        self.vpaned_bottom.set_size_request(50, 50)

        # hpaned_work_area
        # -----------------------------------------------------
        # | vbox_left      ||   work_area
        # -----------------------------------------------------
        vbox_left: Gtk.VBox = Gtk.VBox(homogeneous=False, spacing=0)
        self.hpaned_work_area.add1(vbox_left)
        self.hpaned_work_area.add2(self.work_area)

        # vbox_left
        # -----------------------------------------------------
        # |search
        # -----------------------------------------------------
        # |vpaned_left
        # -----------------------------------------------------

        vbox_left.pack_start(self.search, False, False, 0)
        self.vpaned_left: Gtk.VPaned = Gtk.VPaned()
        vbox_left.pack_start(self.vpaned_left, True, True, 0)

        # vpaned_left
        # -----------------------------------------------------
        # |blocks_tree_view
        # =====================================================
        # |property_box
        # -----------------------------------------------------

        self.vpaned_left.add1(self.__create_frame(self.block_notebook))
        self.vpaned_left.add2(self.__create_frame(self.property_box))
        self.vpaned_left.set_position(System.get_preferences().vpaned_left)

        self.connect("key-press-event", self.__on_key_press)
        self.connect("check-resize", self.__resize)
        self.connect("delete-event", self.main_control.exit)

        self.main_control.init()

        # Load the plugin
        from mosaicode.plugins.extensionsmanager.extensionsmanager \
            import ExtensionsManager as em
        em().load(self)

    # ----------------------------------------------------------------------
    def __create_frame(self, widget: Gtk.Widget) -> Gtk.Frame:
        """
        This method create a frame for widget.

        Parameters:
            * **widget** (:class:`Gtk.Widget`)

        Returns:
            * **Gtk.Frame**
        """
        frame: Gtk.Frame = Gtk.Frame()
        frame.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        frame.add(widget)
        return frame

    # ----------------------------------------------------------------------
    def __resize(self, widget: Optional[Gtk.Widget] = None, data: Optional[Any] = None) -> None:
        """
        This method resize the window.

        Parameters:
            * **widget** (:class:`Gtk.Widget`)
            * **data** (:class:`Any`)

        Returns:
            * **None**
        """
        if widget is None:
            return
        
        width: int
        height: int
        width, height = self.get_window_size()
        
        preferences = System.get_preferences()
        preferences.width = width
        preferences.height = height
        preferences.hpaned_work_area = self.hpaned_work_area.get_position()
        preferences.vpaned_bottom = self.vpaned_bottom.get_position()
        preferences.vpaned_left = self.vpaned_left.get_position()

    # ----------------------------------------------------------------------
    def __on_key_press(self, widget: Gtk.Widget, event: Gdk.EventKey) -> bool:
        """
        This method handle key press events.

        Parameters:
            * **widget** (:class:`Gtk.Widget`)
            * **event** (:class:`Gdk.EventKey`)

        Returns:
            * **bool**
        """
        key: int = event.keyval
        state: int = event.state
        
        # Ctrl+S - Save
        if key == Gdk.KEY_s and state & Gdk.ModifierType.CONTROL_MASK:
            self.main_control.save()
            return True
        
        # Ctrl+O - Open
        if key == Gdk.KEY_o and state & Gdk.ModifierType.CONTROL_MASK:
            self.main_control.select_open()
            return True
        
        # Ctrl+N - New
        if key == Gdk.KEY_n and state & Gdk.ModifierType.CONTROL_MASK:
            self.main_control.new()
            return True
        
        # Ctrl+Z - Undo
        if key == Gdk.KEY_z and state & Gdk.ModifierType.CONTROL_MASK:
            self.main_control.undo()
            return True
        
        # Ctrl+Y - Redo
        if key == Gdk.KEY_y and state & Gdk.ModifierType.CONTROL_MASK:
            self.main_control.redo()
            return True
        
        # Delete key
        if key == Gdk.KEY_Delete:
            self.main_control.delete()
            return True
        
        return False

    # ----------------------------------------------------------------------
    def get_window_size(self) -> tuple[int, int]:
        """
        Get the window size.

        Returns:
            tuple[int, int]: (width, height)
        """
        return super().get_size()

    # ----------------------------------------------------------------------
    def get_property_box(self) -> PropertyBox:
        """
        Get the property box.

        Returns:
            PropertyBox: The property box instance
        """
        return self.property_box

    # ----------------------------------------------------------------------
    def get_work_area(self) -> WorkArea:
        """
        Get the work area.

        Returns:
            WorkArea: The work area instance
        """
        return self.work_area

    # ----------------------------------------------------------------------
    def get_status(self) -> Status:
        """
        Get the status bar.

        Returns:
            Status: The status bar instance
        """
        return self.status

    # ----------------------------------------------------------------------
    def get_main_control(self) -> MainControl:
        """
        Get the main control.

        Returns:
            MainControl: The main control instance
        """
        return self.main_control

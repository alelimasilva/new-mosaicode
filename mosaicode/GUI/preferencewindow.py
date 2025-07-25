#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains the PreferenceWindow class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from mosaicode.system import System as System
from mosaicode.GUI.fields.stringfield import StringField
from mosaicode.GUI.fields.openfilefield import OpenFileField
from mosaicode.GUI.fields.intfield import IntField
import gettext
from typing import Any, Dict, List, Optional, Union

_ = gettext.gettext


class PreferenceWindow(Gtk.Dialog):
    """
    This class contains methods related the PreferenceWindow class
    """

    def __init__(self, main_window) -> None:
        """
        This method is the constructor.
        """
        Gtk.Dialog.__init__(self,
                    title=_("Preferences"),
                    transient_for=main_window)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)

        self.main_window = main_window
        self.properties = System.get_preferences()
        box = self.get_content_area()
        box.set_border_width(3)

        self.tabs = Gtk.Notebook()
        box.add(self.tabs)

        # User preferences
        # ----------------------------------------------------------------------
        self.user_preferences_tab = Gtk.Box()
        self.user_preferences_tab.set_border_width(10)
        label = Gtk.Label(label=_("User Preferences"))
        self.tabs.append_page(self.user_preferences_tab, label)
        self.__create_user_preferences_tab()

        # Default directory
        # ----------------------------------------------------------------------
        self.default_directory_tab = Gtk.Box()
        self.default_directory_tab.set_border_width(10)
        label = Gtk.Label(label=_("Default Directory"))
        self.tabs.append_page(self.default_directory_tab, label)
        self.__create_default_directory_tab()

        # Grid Preferences
        # ----------------------------------------------------------------------
        self.grid_preferences_tab = Gtk.Box()
        self.grid_preferences_tab.set_border_width(10)
        label = Gtk.Label(label=_("Grid Preferences"))
        self.tabs.append_page(self.grid_preferences_tab, label)
        self.__create_grid_preferences_tab()

        self.show_all()

    # ----------------------------------------------------------------------
    def run(self) -> Any:
        response = super(Gtk.Dialog, self).run()

        if response == Gtk.ResponseType.OK:
            self.properties.author = self.author.get_value()
            self.properties.license = self.license.get_value()
            self.properties.default_directory = self.default_directory.get_value()
            self.properties.default_filename = self.default_filename.get_value()
            self.properties.grid = self.grid.get_value()
            self.main_window.main_control.redraw(None)

        self.close()
        self.destroy()

    # Default directory
    # ----------------------------------------------------------------------
    def __create_user_preferences_tab(self):
        vbox = Gtk.VBox()
        self.user_preferences_tab.pack_start(vbox, True, True, 0)

        data = {"label": _("User Name:"),
                "value": self.properties.author}
        self.author = StringField(data, None)
        vbox.pack_start(self.author, False, True, 0)

        data = {"label": _("Generate Code License:"),
                "value": self.properties.license}
        self.license = StringField(data, None)
        vbox.pack_start(self.license, False, True, 0)

        self.user_preferences_tab.show_all()

    # Default directory
    # ----------------------------------------------------------------------
    def __create_default_directory_tab(self):
        vbox = Gtk.VBox()
        self.default_directory_tab.pack_start(vbox, True, True, 0)

        data = {"label": _("Default directory:"),
                "value": self.properties.default_directory}
        self.default_directory = OpenFileField(data, None)
        vbox.pack_start(self.default_directory, False, True, 0)

        # Default directory
        data = {"label": _("Default Filename:"),
                "value": self.properties.default_filename}
        self.default_filename = StringField(data, None)
        vbox.pack_start(self.default_filename, False, True, 0)

        vbox.pack_start(Gtk.Label(label=_("\nName Wildcards:\n" +
                             "\t%d = Date | %n = diagram name |"
                             " %t = time value | %l = language\n")),
                             False, True, 0)

        self.default_directory_tab.show_all()

    # Grid Preferences
    # ----------------------------------------------------------------------
    def __create_grid_preferences_tab(self):
        vbox = Gtk.VBox()
        self.grid_preferences_tab.pack_start(vbox, True, True, 0)

        data = {"label": _("Grid size"), "value": self.properties.grid}
        self.grid = IntField(data, None)
        vbox.pack_start(self.grid, False, True, 0)

        self.grid_preferences_tab.show_all()


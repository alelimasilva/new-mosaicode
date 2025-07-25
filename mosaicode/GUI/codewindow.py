#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# noqa: E402
"""
This module contains the CodeWindow class.
"""
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '3.0')
from gi.repository import Gtk, GtkSource
import gettext
_ = gettext.gettext


class CodeWindow(Gtk.Dialog):

    """
    This class contains the methods related to CodeWindow class.
    """

    # ----------------------------------------------------------------------

    def __init__(self, main_window, codes):
        """
        This method is the constructor.
        """
        Gtk.Dialog.__init__(self,
                        title="Code Window",
                        transient_for=main_window,
                        modal=True,
                        destroy_with_parent=True)
        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.codes = codes
        self.main_window = main_window
        self.set_default_size(800, 600)
        box = self.get_content_area()
        vbox = Gtk.VBox()
        box.pack_start(vbox, True, True, 0)

        toolbar = Gtk.Toolbar()
        toolbar.set_style(Gtk.ToolbarStyle.BOTH)
        toolbar.set_hexpand(False)
        toolbar.set_property("expand", False)
        vbox.pack_start(toolbar, False, False, 0)


        icon_size = Gtk.IconSize.LARGE_TOOLBAR
        icon = Gtk.Image.new_from_icon_name(Gtk.STOCK_SAVE_AS, icon_size)
        self.save_button = Gtk.ToolButton.new(icon, _("Save Source"))
        self.save_button.set_expand(False)
        self.save_button.set_is_important(True)
        self.save_button.connect("clicked", self.__save_button_clicked, None)
        toolbar.add(self.save_button)

        icon = Gtk.Image.new_from_icon_name(Gtk.STOCK_EXECUTE, icon_size)
        self.run_button = Gtk.ToolButton.new(icon, _("Run this code"))
        self.run_button.set_expand(False)
        self.run_button.set_is_important(True)
        self.run_button.connect("clicked", self.__run_button_clicked, None)
        toolbar.add(self.run_button)


        self.notebook = Gtk.Notebook()
        vbox.pack_start(self.notebook, True, True, 0)

        self.buffers = {}

        for key in self.codes:
            code = self.codes[key]
            lang_manager = GtkSource.LanguageManager()
            textbuffer = GtkSource.Buffer.new_with_language(
                lang_manager.get_language('c'))
            textview = GtkSource.View.new_with_buffer(textbuffer)
            textview.set_show_line_numbers(True)
            textview.set_left_margin(10)
            textview.set_right_margin(10)
            textview.get_buffer().set_text(code)
            self.buffers[key] = textview.get_buffer()

            sw = Gtk.ScrolledWindow()
            sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
            sw.add(textview)
            textview.show()
            self.notebook.append_page(sw, Gtk.Label(label=key))
        self.show_all()

    # ----------------------------------------------------------------------
    def __load_buffers(self):
        """
        This method monitors if the button was clicked.

            Parameters:

        """
        for key in self.buffers:
            self.codes[key] = self.buffers[key].get_text(
                        self.buffers[key].get_start_iter(),
                        self.buffers[key].get_end_iter(),
                        True)

    # ----------------------------------------------------------------------
    def __save_button_clicked(self, widget, data):
        """
        This method monitors if the button was clicked.

            Parameters:

        """
        self.__load_buffers()
        self.main_window.main_control.save_source(self.codes)

    # ----------------------------------------------------------------------
    def __run_button_clicked(self, widget, data):
        """
        This method monitors if the button was clicked.

            Parameters:

        """
        self.__load_buffers()
        self.main_window.main_control.run(self.codes)

# ----------------------------------------------------------------------

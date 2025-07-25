#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains the Toolbar class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import gettext
from typing import Any, Dict, List, Optional, Union
_ = gettext.gettext


class Toolbar(Gtk.Toolbar):
    """
    This class contains methods related the Toolbar class.
    """

    # ----------------------------------------------------------------------
    def __init__(self, main_window) -> None:
        """
        This method is the constructor is creates each menu button.
        """
        Gtk.Toolbar.__init__(self)
        self.main_window = main_window
        self.set_style(Gtk.ToolbarStyle.BOTH)
        self.set_hexpand(False)
        self.set_property("expand", False)

        self.actions: Dict[str, Any] = {}
        self.__create_button(Gtk.STOCK_NEW,
                             _("New"),
                             self.main_window.main_control.new)
        self.__create_button(Gtk.STOCK_OPEN,
                             _("Open Project"),
                             self.main_window.main_control.select_open)
        self.__create_button(Gtk.STOCK_SAVE,
                             _("Save Project"),
                             self.main_window.main_control.save)

        self.add(Gtk.SeparatorToolItem())

        # Criar menu dropdown para o botão Run
        self.run_menu = Gtk.Menu()
        
        # Opção "Run" (rodar sem salvar)
        self.run_menu_item = Gtk.MenuItem.new_with_label(_("Run"))
        self.run_menu_item.connect("activate", self.__run_clicked, None)
        self.run_menu.append(self.run_menu_item)
        
        # Opção "Save" (salvar arquivos)
        self.save_menu_item = Gtk.MenuItem.new_with_label(_("Save"))
        self.save_menu_item.connect("activate", self.__save_clicked, None)
        self.run_menu.append(self.save_menu_item)
        # Removida a opção "Save and Run"

        self.__create_button(Gtk.STOCK_EXECUTE,
                             _("Run"),
                             self.__run_button_clicked,
                             self.run_menu)

        self.__create_button(Gtk.STOCK_SELECT_ALL,
                             _("View Source"),
                             self.main_window.main_control.view_source)

        self.add(Gtk.SeparatorToolItem())
        self.__create_button(Gtk.STOCK_ZOOM_OUT,
                             _("Zoom Out"),
                             self.main_window.main_control.zoom_out)
        self.__create_button(Gtk.STOCK_ZOOM_IN,
                             _("Zoom In"),
                             self.main_window.main_control.zoom_in)
        self.__create_button(Gtk.STOCK_ZOOM_100,
                             _("Normal Size"),
                             self.main_window.main_control.zoom_normal)

        self.show_all()

    # ----------------------------------------------------------------------
    def __create_button(self, stock, name, action, menu=None):
        """
        This method create a button on menu.

            Parameters:
            Returns:

        """
        icon_size = Gtk.IconSize.LARGE_TOOLBAR
        icon = Gtk.Image.new_from_icon_name(stock, icon_size)
        if menu is None:
            button = Gtk.ToolButton.new(icon, name)
        else:
            button = Gtk.MenuToolButton.new(icon, name)
            button.set_menu(menu)
        button.set_expand(False)
        button.set_label(name)
        button.set_is_important(True)
        button.connect("clicked", self.__button_clicked, None)
        self.add(button)
        self.actions[button] = action
        return button

    # ----------------------------------------------------------------------
    def update_threads(self, threads) -> None:
        for widget in self.run_menu.get_children():
            self.run_menu.remove(widget)
        for thread in threads:
            diagram, process = threads[thread]
            icon = Gtk.Image.new_from_icon_name(Gtk.STOCK_STOP, Gtk.IconSize.MENU)
            box = Gtk.HBox()
            box.add(Gtk.Label.new(diagram.patch_name))
            box.add(icon)
            item = Gtk.MenuItem()
            item.add(box)
            item.connect("activate",
                        self.main_window.main_control.stop,
                        process)
            self.run_menu.append(item)
        self.run_menu.show_all()

    # ----------------------------------------------------------------------
    def __button_clicked(self, widget, data):
        """
        This method monitors if the button was clicked.

            Parameters:

        """
        if widget in self.actions:
            self.actions[widget]()

    # ----------------------------------------------------------------------
    def __run_button_clicked(self, widget=None, data=None):
        """
        Handler para o clique no botão Run principal.
        Executa imediatamente (igual ao menu Process > Run).
        """
        self.main_window.main_control.execute_only()
        # O menu dropdown continua disponível ao clicar na seta

    # ----------------------------------------------------------------------
    def __run_clicked(self, widget, data):
        """
        Handler para a opção "Run" do menu.
        Executa sem salvar, usando salvamento temporário.
        """
        self.main_window.main_control.execute_only()

    # ----------------------------------------------------------------------
    def __save_clicked(self, widget, data):
        """
        Handler para a opção "Save" do menu.
        Salva os arquivos no local escolhido.
        """
        self.main_window.main_control.save_source_only()

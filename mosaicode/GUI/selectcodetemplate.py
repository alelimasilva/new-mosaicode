#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains the PreferenceWindow class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from mosaicode.GUI.fields.combofield import ComboField

import gettext
from typing import Any, Dict, List, Optional, Union

_ = gettext.gettext


class SelectCodeTemplate(Gtk.Dialog):
    """
    This class contains methods related the PreferenceWindow class
    """

    def __init__(self, main_window, template_list) -> None:
        """
        This method is the constructor.
        """
        Gtk.Dialog.__init__(self,
                    title=_("Select Code Template"),
                    transient_for=main_window)
        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)

        self.template_list = template_list

        templates = []
        for code_template in template_list:
            templates.append(code_template.description)

        data = {"label": _("Code Template"), "name":"template", "values": templates}
        self.field = ComboField(data, None)
        self.field.field.set_active(0)
        self.get_content_area().add(self.field)

    # ----------------------------------------------------------------------
    def get_value(self) -> Any:
        self.show_all()
        response = self.run()
        index = self.field.field.get_active()
        if index == -1:
            return None
        template = self.template_list[index]
        self.close()
        self.destroy()
        return self.template_list[index]

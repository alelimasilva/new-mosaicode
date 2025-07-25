#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains the CheckField class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from mosaicode.GUI.fields.field import Field
from typing import Any, Dict, List, Optional, Union


class CheckField(Field):
    """
    This class contains methods related the CheckField class.
    """
    # ------------------------------------------------------------------------------

    configuration = {"label": "", "value": False, "name": ""}

    def __init__(self, data, event) -> None:
        """
        This method is the constructor.
        """
        if not isinstance(data, dict):
            return
        Field.__init__(self, data, event)

        self.check_values()
        self.create_label()

        self.field = Gtk.Switch()
        self.field.set_property("margin-left", 20)
        self.field.set_property("halign", Gtk.Align.END)

        if isinstance(self.data["value"], str) \
                or isinstance(self.data["value"], bytes):
            if self.data["value"] == "True":
                self.field.set_active(True)
            else:
                self.field.set_active(False)
        elif isinstance(self.data["value"], bool):
            self.field.set_active(self.data["value"])

        if event is not None:
            self.field.connect("notify::active", event)
        self.add(self.field)
        self.show_all()

    # ------------------------------------------------------------------------------
    def get_value(self) -> Any:
        """
        This method get the value.
        """
        return self.field.get_active()

    # ------------------------------------------------------------------------------
    def set_value(self, value) -> None:
        """
        This method set the value.
        """
        return self.field.set_active(value)

# ------------------------------------------------------------------------------

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains the IntField class.
"""
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from mosaicode.GUI.fields.field import Field
from typing import Any, Dict, List, Optional, Union


class IntField(Field):
    """
    This class contains methods related the IntField class.
    """

    configuration = {
        "label": "",
        "value": 0,
        "name": "",
        "lower": -(sys.maxsize - 1),
        "upper": sys.maxsize,
        "step": 1,
        "page_increment": 10,
        "page_size": 10
    }

    # ------------------------------------------------------------------------------
    def __init__(self, data, event) -> None:
        """
        This method is the constructor.
        """
        if not isinstance(data, dict):
            return
        Field.__init__(self, data, event)

        self.check_values()
        self.create_label()

        adjustment = Gtk.Adjustment(value=float(self.data["value"]),
                                lower=int(self.data["lower"]),
                                upper=int(self.data["upper"]),
                                step_increment=int(self.data["step"]),
                                page_increment=int(self.data["page_increment"]),
                                page_size=int(self.data["page_size"]))
        self.field = Gtk.SpinButton()
        self.field.set_property("margin-left", 20)
        self.field.set_adjustment(adjustment)
        self.field.set_value(float(self.data["value"]))

        if event is not None:
            self.field.connect("changed", event)
            self.field.connect("value-changed", event)
            self.field.connect("change-value", event)
        self.add(self.field)
        self.show_all()

    # ------------------------------------------------------------------------------
    def get_value(self) -> Any:
        return int(self.field.get_value())

    # --------------------------------------------------------------------------
    def set_value(self, value) -> None:
        self.field.set_value(float(value))

# ------------------------------------------------------------------------------

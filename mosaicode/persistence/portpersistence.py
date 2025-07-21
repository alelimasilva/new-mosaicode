# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the PortPersistence class.
"""
from pathlib import Path
import inspect  # For module inspect
import pkgutil  # For dynamic package load
import json
from mosaicode.model.port import Port
from mosaicode.persistence.persistence import Persistence
from typing import Dict, List, Optional, Any, Union


class PortPersistence():
    """
    This class contains methods related the PortPersistence class.
    """

    # ----------------------------------------------------------------------
    @classmethod
    def load(cls, file_name):
        """
        This method loads the port from XML file.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        # load the port
        if not Path(file_name).exists():
            return None

        data = ""
        port = Port()

        try:
            with open(file_name, 'r') as data_file:
                data = json.load(data_file)

            if data["data"] != "PORT":
                return None

            port = Port()
            port.type = data["type"]
            port.version = data["version"]
            port.type = data["type"]
            port.language = data["language"]
            port.hint = data["hint"]
            if not port.hint:
                port.hint = f"[{port.type.upper()}]"
            port.color = data["color"]
            port.multiple = bool(data["multiple"])
            port.var_name = data["var_name"]
            port.code = data["code"]
        except (IOError, OSError) as e:
            return None

        if port.type == "":
            return None

        return port

    # ----------------------------------------------------------------------
    @classmethod
    def save(cls, port, path):
        """
        This method save the port in user space.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        x = {
          "source": "JSON",
          "data": "PORT",
          "version": port.version,
          "type": port.type,
          "language": port.language,
          "hint": port.hint,
          "color": port.color,
          "multiple": port.multiple,
          "var_name": port.var_name,
          "code": port.code
        }
        
        if not Persistence.create_dir(path):
            return False
        try:
            file_path = Path(path) / f"{port.type}.json"
            with open(file_path, 'w') as data_file:
                data_file.write(json.dumps(x, indent=4))

        except IOError as e:
            return False
        return True

# ----------------------------------------------------------------------

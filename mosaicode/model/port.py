# -*- coding: utf-8 -*-
"""
This module contains the Port class.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Union
from pathlib import Path


class ConnectionType(Enum):
    """Enum for port connection types."""
    INPUT = "input"
    OUTPUT = "output"


@dataclass
class Port:
    """
    This class contains the base attributes of each block port.
    """
    INPUT = ConnectionType.INPUT.value
    OUTPUT = ConnectionType.OUTPUT.value

    # Attributes defined by the Ports
    type: str = field(default_factory=lambda: Port.__module__)
    version: str = field(default_factory=lambda: Port._get_version())
    language: str = ""
    hint: str = ""
    color: str = "#000"
    multiple: bool = False
    file: Optional[Union[str, Path]] = None
    code: str = ""
    var_name: str = "$block[label]$_$block[id]$_$port[name]$"
    
    # Attributes defined in Block Ports
    conn_type: Optional[str] = None
    name: Optional[str] = None
    label: Optional[str] = None
    index: int = -1
    type_index: int = -1
    
    def __post_init__(self) -> None:
        """Initialize after dataclass creation."""
        # Load default values from JSON template if not already set
        if self.version == Port._get_version():
            self._load_defaults()
    
    @staticmethod
    def _get_version() -> str:
        """Get system version."""
        from mosaicode.system import System
        return System.VERSION
    
    def _load_defaults(self) -> None:
        """Load default values from JSON template."""
        from mosaicode.system import System
        from mosaicode.utils.config_loader import ConfigLoader
        
        # Load port defaults
        defaults = ConfigLoader.load_template("defaults", "ports")
        default_values = defaults.get("default_values", {})
        
        # Set default values only if not already set
        if self.version == Port._get_version():
            self.version = default_values.get("version", System.VERSION)
        if self.language == "":
            self.language = default_values.get("language", "")
        if self.hint == "":
            self.hint = default_values.get("hint", "")
        if self.color == "#000":
            self.color = default_values.get("color", "#000")
        if not self.multiple:
            self.multiple = default_values.get("multiple", False)
        if self.file is None:
            self.file = default_values.get("file")
        if self.code == "":
            self.code = default_values.get("code", "")
        if self.var_name == "$block[label]$_$block[id]$_$port[name]$":
            self.var_name = default_values.get("var_name", "$block[label]$_$block[id]$_$port[name]$")
        
        # Attributes defined in Block Ports
        if self.conn_type is None:
            self.conn_type = default_values.get("conn_type")
        if self.name is None:
            self.name = default_values.get("name")
        if self.label is None:
            self.label = default_values.get("label")
        if self.index == -1:
            self.index = default_values.get("index", -1)
        if self.type_index == -1:
            self.type_index = default_values.get("type_index", -1)

    # ----------------------------------------------------------------------
    def is_input(self) -> bool:
        """Check if this port is an input port."""
        return str(self.conn_type).lower() == self.INPUT

    # ----------------------------------------------------------------------
    def is_output(self) -> bool:
        """Check if this port is an output port."""
        return str(self.conn_type).lower() == self.OUTPUT

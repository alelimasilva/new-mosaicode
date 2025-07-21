#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains the BlockModel class.
"""
from dataclasses import dataclass, field
from functools import cached_property
from typing import Dict, List, Optional, Any, Union
from pathlib import Path


@dataclass
class BlockModel:
    """
    This class contains the base attributes of each block,
    their position on the screen, id and others applicable properties for
    each one.
    """

    # Basic attributes
    id: int = field(default_factory=lambda: -1)
    version: str = field(default_factory=lambda: BlockModel._get_version())
    x: int = 0
    y: int = 0
    is_collapsed: bool = False
    
    # Type and language
    type: str = field(default_factory=lambda: BlockModel.__module__)
    language: str = ""
    extension: str = ""
    file: Optional[Union[str, Path]] = None
    
    # Appearance
    help: str = ""
    label: str = "A"
    color: str = "#000000"
    group: str = "Undefined"
    ports: List[Any] = field(default_factory=list)
    maxIO: int = 0
    
    # Code generation
    properties: List[Dict[str, Any]] = field(default_factory=list)
    codes: Dict[str, str] = field(default_factory=dict)
    gen_codes: Dict[str, str] = field(default_factory=dict)
    
    # Attributes to code generation
    weight: int = 0
    connections: List[Any] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        """Initialize after dataclass creation."""
        # Load default values from JSON template if not already set
        if self.id == -1:
            self._load_defaults()
    
    @staticmethod
    def _get_version() -> str:
        """Get system version."""
        from mosaicode.system import System
        return System.VERSION
    
    @cached_property
    def properties_dict(self) -> Dict[str, Any]:
        """
        Get properties as a dictionary for easy access.
        
        Returns:
            Dictionary mapping property names to values
        """
        return {prop.get("name", f"prop_{i}"): prop.get("value", "") 
                for i, prop in enumerate(self.properties)}
    
    @cached_property
    def input_ports(self) -> List[Any]:
        """
        Get only input ports.
        
        Returns:
            List of input ports
        """
        return [port for port in self.ports if hasattr(port, 'conn_type') and port.conn_type == 'input']
    
    @cached_property
    def output_ports(self) -> List[Any]:
        """
        Get only output ports.
        
        Returns:
            List of output ports
        """
        return [port for port in self.ports if hasattr(port, 'conn_type') and port.conn_type == 'output']
    
    @cached_property
    def port_count(self) -> int:
        """
        Get total number of ports.
        
        Returns:
            Number of ports
        """
        return len(self.ports)
    
    @cached_property
    def has_properties(self) -> bool:
        """
        Check if block has properties.
        
        Returns:
            True if block has properties, False otherwise
        """
        return len(self.properties) > 0
    
    @cached_property
    def display_label(self) -> str:
        """
        Get display label for the block.
        
        Returns:
            Display label (label or type if label is generic)
        """
        if self.label and self.label not in ["A", ""]:
            return self.label
        return self.type.replace("_", " ").title()
    
    def _load_defaults(self) -> None:
        """Load default values from JSON template."""
        try:
            from mosaicode.utils.config_loader import ConfigLoader
            defaults = ConfigLoader.load_template("defaults", "blocks")
            if defaults and "default_values" in defaults:
                default_values = defaults["default_values"]
                for key, value in default_values.items():
                    if hasattr(self, key) and getattr(self, key) in [0, "", False, [], {}]:
                        setattr(self, key, value)
        except Exception as e:
            # Log error but don't fail initialization
            import logging
            logger = logging.getLogger(__name__)
            logger.debug(f"Failed to load defaults for block: {e}")

    # ----------------------------------------------------------------------
    def get_color_as_rgba(self) -> str:
        """
        Returns the color in RGBA format.

        Returns:
            * **Types**: :class:`str<str>`
            The return is the RGBA color. The hex value is a **str** type.
        """

        if self.color.startswith("#"):
            return self.color
        return f"rgba({self.color.replace(':', ',')})"

    # ----------------------------------------------------------------------
    def get_color(self) -> str:
        """
        Returns the color value.

        Returns:
            * **Types**: :class:`str<str>`
            The return is the color value.
        """
        return self.color

    # ----------------------------------------------------------------------
    def set_properties(self, data: Dict[str, Any]) -> None:
        """Set properties from data dictionary."""
        for prop in self.get_properties():
            key = prop.get("name")
            if key in data:
                prop["value"] = data[key]
            else:
                # Import System here to avoid circular import
                from mosaicode.system import System
                System.log(f"BlockModel.set_property ({self.type}) ERROR: key {key} not present")

    # ----------------------------------------------------------------------
    def get_properties(self) -> List[Dict[str, Any]]:
        """Get all properties."""
        return self.properties

    # ----------------------------------------------------------------------
    def __str__(self) -> str:
        return str(self.id)

# ------------------------------------------------------------------------------

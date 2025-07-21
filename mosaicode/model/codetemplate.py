#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains the CodeTemplate class.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from pathlib import Path


@dataclass
class CodeTemplate:
    """
    This class contains the base attributes of each code generator.
    """

    # Basic attributes
    type: str = field(default_factory=lambda: CodeTemplate.__module__)
    version: int = 0
    name: str = ""
    file: Optional[Union[str, Path]] = None
    description: str = ""
    language: str = ""
    command: str = ""
    
    # Code generation
    codes: Dict[str, str] = field(default_factory=dict)
    code_parts: List[Any] = field(default_factory=list)
    properties: List[Dict[str, Any]] = field(default_factory=list)

    # ----------------------------------------------------------------------
    def equals(self, code_template: 'CodeTemplate') -> bool:
        """
        Compare this code template with another.
        
        Args:
            code_template: The code template to compare with
            
        Returns:
            True if templates are equal, False otherwise
        """
        for key in self.__dict__:
            if not hasattr(code_template, key):
                return False
            if code_template.__dict__[key] != self.__dict__[key]:
                return False
        return True

    # ----------------------------------------------------------------------
    def set_properties(self, data: Dict[str, Any]) -> None:
        """
        Set properties from data dictionary.
        
        Args:
            data: Dictionary containing property values
        """
        for prop in self.get_properties():
            key = prop.get("name")
            if key in data:
                prop["value"] = data[key]

    # ----------------------------------------------------------------------
    def get_properties(self) -> List[Dict[str, Any]]:
        """
        Get all properties.
        
        Returns:
            List of property dictionaries
        """
        return self.properties

    # ----------------------------------------------------------------------
    def __str__(self) -> str:
        return str(self.type)

# ------------------------------------------------------------------------------

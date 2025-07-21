#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains the CommentModel class.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class CommentModel:
    """
    This class contains the base attributes of each comment,
    their position on the screen, id and others applicable properties for
    each one.
    """

    # Basic attributes
    id: int = -1
    x: int = 0
    y: int = 0
    properties: List[Dict[str, Any]] = field(default_factory=lambda: [
        {
            "label": "Text",
            "name": "text",
            "value": "Comment",
            "type": CommentModel._get_comment_type(),
        }
    ])
    
    @staticmethod
    def _get_comment_type() -> str:
        """Get comment field type."""
        # Import fieldtypes here to avoid GTK dependency during module import
        from mosaicode.GUI.fieldtypes import MOSAICODE_COMMENT
        return MOSAICODE_COMMENT

    # ----------------------------------------------------------------------
    def set_properties(self, data: Optional[Dict[str, Any]]) -> None:
        """Set properties from data dictionary."""
        if data is None:
            return
        if self.get_properties() is None:
            self.properties = []
        for prop in self.get_properties():
            key = prop.get("name")
            if key in data:
                prop["value"] = data[key]

    # ----------------------------------------------------------------------
    def get_properties(self) -> List[Dict[str, Any]]:
        """Get all properties."""
        return self.properties

    # ----------------------------------------------------------------------
    def __str__(self) -> str:
        """Return comment text as string representation."""
        if self.properties is None:
            self.properties = []
        if len(self.properties) < 1:
            return ""
        if "value" in self.properties[0]:
            return str(self.properties[0]["value"])
        return ""

# ------------------------------------------------------------------------------

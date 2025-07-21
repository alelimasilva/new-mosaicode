# -*- coding: utf-8 -*-
"""
This module contains the DiagramModel class.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path


@dataclass
class DiagramModel:
    """
    This class contains the diagram model with blocks, connectors, and metadata.
    """
    
    # Basic attributes
    last_id: int = 1  # first block is n1, increments to each new block
    blocks: Dict[str, Any] = field(default_factory=dict)  # GUI blocks
    connectors: List[Any] = field(default_factory=list)
    comments: List[Any] = field(default_factory=list)
    code_template: Optional[Any] = None

    # Display and state
    zoom: float = 1.0  # pixels per unit
    file_name: str = "Untitled"
    modified: bool = False
    language: Optional[str] = None
    undo_stack: List[Any] = field(default_factory=list)
    redo_stack: List[Any] = field(default_factory=list)
    authors: List[str] = field(default_factory=list)

    # ----------------------------------------------------------------------
    @property
    def patch_name(self) -> str:
        """Extract patch name from file path."""
        name = self.file_name
        if "/" in name or "\\" in name:
            # Use pathlib for cross-platform path handling
            path = Path(name)
            name = path.stem  # Get filename without extension
        else:
            # Handle case where name might have extension
            name = Path(name).stem
        return name

    # ----------------------------------------------------------------------
    def __str__(self) -> str:
        return str(self.patch_name)

# ------------------------------------------------------------------------------

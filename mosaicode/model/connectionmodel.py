#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains the ConnectionModel class.
"""
from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class ConnectionModel:
    """
    This class represents a connection between two blocks in a diagram.
    """

    def __init__(
        self, 
        diagram: Any, 
        output: Any, 
        output_port: Any, 
        input: Optional[Any] = None, 
        input_port: Optional[Any] = None
    ):
        """
        Initialize a connection model.
        
        Args:
            diagram: The diagram containing this connection
            output: The output block
            output_port: The output port
            input: The input block (optional)
            input_port: The input port (optional)
        """
        self.output: Any = output
        self.output_port: Any = output_port
        self.input: Optional[Any] = input
        self.input_port: Optional[Any] = input_port
        self.diagram: Any = diagram

# -----------------------------------------------------------------------------

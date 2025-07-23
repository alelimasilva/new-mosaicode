# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the BlockControl class.
"""
import ast
import copy
import inspect  # For module inspect
from pathlib import Path
import logging
import pkgutil  # For dynamic package load
from typing import Dict, List, Optional, Any

from mosaicode.model.port import Port
from mosaicode.persistence.blockpersistence import BlockPersistence
from mosaicode.model.blockmodel import BlockModel


class BlockControl:
    """
    This class contains methods related the BlockControl class.
    """

    # ----------------------------------------------------------------------

    def __init__(self) -> None:
        """Initialize BlockControl."""
        pass

    # ----------------------------------------------------------------------
    @classmethod
    def load_ports(cls, block: 'BlockModel', ports: Dict[str, Port]) -> None:
        """
        Load ports for a block.
        
        Args:
            block: The block to load ports for
            ports: Dictionary of available ports
        """
        # Adjust ports attributes
        i: int = 0
        in_port: int = 0
        out_port: int = 0
        new_ports: List[Port] = []
        
        for port in block.ports:
            # Se a porta já é um objeto Port, apenas ajustar os índices
            if isinstance(port, Port):
                port.index = i
                if port.is_input():
                    port.type_index = in_port
                    in_port += 1
                else:
                    port.type_index = out_port
                    out_port += 1
                new_ports.append(port)
                i += 1
                continue
                
            # Se é um dicionário (formato antigo), processar como antes
            if not isinstance(port, dict):
                from mosaicode.system import System
                System.log("Error Loading a Block: Port is not a dictionary?");
                continue
            if "type" not in port:
                from mosaicode.system import System
                System.log("Error Loading a Block: Port should have a type");
                continue
            port_type: str = port["type"]
            # Create a copy from the port instance loaded in the System
            if port_type not in ports:
                from mosaicode.system import System
                System.log("Error Loading a Block: Port is not present in System");
                continue
            new_port: Port = copy.deepcopy(ports[port_type])

            if "conn_type" not in port:
                port["conn_type"] = Port.INPUT
            if port["conn_type"].upper() == "INPUT":
                new_port.conn_type = Port.INPUT
            else:
                new_port.conn_type = Port.OUTPUT

            new_port.index = i
            if new_port.is_input():
                new_port.type_index = in_port
                in_port += 1
            else:
                new_port.type_index = out_port
                out_port += 1
            new_port.name = port["name"]
            new_port.label = port["label"]
            new_ports.append(new_port)
            i += 1
        block.maxIO = max(in_port, out_port)
        block.ports = new_ports
    # ----------------------------------------------------------------------
    @classmethod
    def load(cls, file_name: str) -> Optional['BlockModel']:
        """
        This method loads the block from JSON file.

        Args:
            file_name: Path to the block file
            
        Returns:
            BlockModel instance or None if loading failed
        """
        block: Optional['BlockModel'] = BlockPersistence.load(file_name)
        return block
    # ----------------------------------------------------------------------
    @classmethod
    def add_new_block(cls, block: 'BlockModel') -> None:
        """
        Add a new block to the system. Always asks user for save location.
        
        Args:
            block: The block to add
        """
        # Ask user for save location
        from mosaicode.system import System
        System()
        
        # This would need to be integrated with the GUI to show a dialog
        # For now, we'll use a default location but log that user choice is preferred
        path: Path = Path(System.get_user_dir()) / "extensions" / block.language / "blocks" / block.extension / block.group
        System.log("Note: User should be prompted for save location in future versions")
        BlockPersistence.save(block, str(path))

    # ----------------------------------------------------------------------
    @classmethod
    def delete_block(cls, block_key: str) -> bool:
        """
        Delete a block from the system.
        
        Args:
            block_key: Key of the block to delete
            
        Returns:
            True if deletion was successful, False otherwise
        """
        from mosaicode.system import System
        blocks: Dict[str, 'BlockModel'] = System.get_blocks()
        if block_key not in blocks:
            return False
        block: 'BlockModel' = blocks[block_key]
        if block.file is not None:
            Path(block.file).unlink(missing_ok=True)
            return True
        else:
            return False

    # ----------------------------------------------------------------------
    @classmethod
    def print_block(cls, block: 'BlockModel') -> None:
        """
        Print block information.
        
        Args:
            block: BlockModel instance to print
        """
        logging.info(r"Block Type: {block.type}")
        logging.info(r"Block Label: {block.label}")
        logging.info(r"Block Language: {block.language}")
        logging.info(r"Block Extension: {block.extension}")
        logging.info(r"Block Group: {block.group}")
        logging.info(r"Block File: {block.file}")
        logging.info(r"Block Help: {block.help}")
        logging.info(r"Block Max IO: {block.maxIO}")
        logging.info(r"Block Properties: {block.properties}")
        logging.info(r"Block Ports Count: {len(block.ports)}")
        logging.info(r"---------------------")

# ----------------------------------------------------------------------

# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the BlockPersistence class.
"""
import copy
import ast
import inspect  # For module inspect
from pathlib import Path
import pkgutil  # For dynamic package load
import json
import logging
from mosaicode.model.blockmodel import BlockModel
from mosaicode.persistence.persistence import Persistence
from typing import Dict, List, Optional, Any, Union

logger = logging.getLogger(__name__)

class BlockPersistence():
    """
    This class contains methods related the BlockPersistence class.
    """

    # ----------------------------------------------------------------------
    @classmethod
    def load(cls, file_name: str) -> Optional[BlockModel]:
        """
        This method loads the block from JSON file.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        if not Path(file_name).exists():
            logger.warning(f"Block file not found: {file_name}")
            return None

        data = ""
        block = BlockModel()

        try:
            with open(file_name, 'r') as data_file:
                data = json.load(data_file)

            if data["data"] != "BLOCK":
                logger.warning(f"Invalid block data format in {file_name}")
                return None

            # Definir o tipo do bloco a partir do JSON
            block.type = data.get("type", "")
            block.language = data.get("language", "")
            block.extension = data.get("extension", "")
            block.help = data.get("help", "")
            block.label = data.get("label", "")
            block.color = data.get("color", "#000000")
            block.group = data.get("group", "Undefined")
            block.version = data.get("version", "0.0.1")

            # Validate and fix generic labels
            if not block.label or block.label == "A" or block.label == "":
                # Use type as fallback label
                block.label = block.type.replace("_", " ").title()
                logger.debug(f"Fixed generic label for {block.type}: '{data.get('label', '')}' -> '{block.label}'")

            codes = data["codes"]
            if isinstance(codes, dict):
                block.codes = codes
            elif isinstance(codes, list):
                for code in codes:
                    block.codes[code["name"]] = code["code"]

            # Propriedades
            props = data["properties"]
            for prop in props:
                # Normalizar propriedades para garantir campos obrigatórios
                prop_norm = {
                    "type": prop.get("type", "string"),
                    "name": prop.get("name", ""),
                    "label": prop.get("label", prop.get("name", "")),
                    "value": prop.get("value", "")
                }
                # Adicionar outros campos se existirem
                for k in prop:
                    if k not in prop_norm:
                        prop_norm[k] = prop[k]
                block.properties.append(prop_norm)

            # Portas
            ports = data["ports"]
            in_port: int = 0
            out_port: int = 0

            for idx, port_data in enumerate(ports):
                from mosaicode.model.port import Port
                from mosaicode.system import System as System
                port = copy.deepcopy(System.get_ports()[port_data.get("type", "")])
                conn_type = port_data.get("conn_type", "OUTPUT")
                if str(conn_type).upper() == "INPUT":
                    port.conn_type = Port.INPUT
                    port.type_index = in_port
                    in_port += 1
                else:
                    port.conn_type = Port.OUTPUT
                    port.type_index = out_port
                    out_port += 1
                port.name = port_data.get("name", "")
                port.label = port_data.get("label", "")
                port.type_index = port_data.get("type_index", idx)
                port.hint = port_data.get("hint", "")
                block.ports.append(port)

            block.maxIO = max(in_port, out_port)

            block.file = str(file_name)

            logger.debug(f"Successfully loaded block: {block.type} with label: '{block.label}'")

        except (IOError, OSError) as e:
            logger.error(f"IO error loading block {file_name}: {e}")
            pass
        except Exception as e:
            logger.error(f"Unexpected error loading block {file_name}: {e}")
            pass

        if block.type == "mosaicode.model.blockmodel":
            logger.warning(f"Invalid block type in {file_name}")
            return None
        return block

    # ----------------------------------------------------------------------
    @classmethod
    def save(cls, block: BlockModel, path: Optional[str] = None) -> bool:
        """
        This method save the block in user space.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """

        x = {
            "source": "JSON",
            "data": "BLOCK",
            "version": block.version,
            "type": block.type,
            "language": block.language,
            "extension": block.extension,
            "help": block.help,
            "label": block.label,
            "color": block.color,
            "group": block.group,
            "codes": [],
            "properties":[],
            "ports":[]
        }
        
        for key in block.codes:
            x["codes"].append({
                "name":key,
                "code": block.codes[key]
                })

        for key in block.properties:
            x["properties"].append(key)

        for port in block.ports:
            x["ports"].append({
                        "conn_type": port.conn_type,
                        "name": port.name,
                        "label": port.label,
                        "type":port.type
                        }
                        )

        if (path is not None) and not Persistence.create_dir(Path(path)):
            from mosaicode.system import System as System
            System.log("Problem saving Blocks")
            return False

        if (path is None) and (block.file is not None):
            path = str(block.file)
        elif (path is not None):
            file_name = block.label
            path = str(Path(path) / f"{file_name}.json")
        else:
            from mosaicode.system import System as System
            System.log("Problem saving Blocks")
            return False

        try:
            with open(str(path), 'w') as data_file:
                data_file.write(json.dumps(x, indent=4))
        except IOError as e:
            from mosaicode.system import System as System
            System.log("Problem saving Blocks")
            return False
        return True
# ----------------------------------------------------------------------

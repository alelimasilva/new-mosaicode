# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the BlockPersistence class.
"""
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

            # Construir tipo completo baseado no caminho do arquivo
            file_path = Path(file_name)
            path_str = str(file_path)
            # Lógica genérica para qualquer extensão que siga o padrão
            blocks_marker = "/extensions/blocks/"
            if blocks_marker in path_str:
                # Extrai o nome do pacote da extensão
                # Exemplo: .../mosaicode-javascript-webaudio/mosaicode_lib_javascript_webaudio/extensions/blocks/arithmetic/add.json
                # Pacote: mosaicode_lib_javascript_webaudio
                # Caminho relativo: arithmetic/add.json
                # Tipo: mosaicode_lib_javascript_webaudio.extensions.blocks.arithmetic.add
                try:
                    # Encontrar início do nome do pacote
                    # Busca pelo último '/' antes de 'extensions/blocks/'
                    idx_blocks = path_str.index(blocks_marker)
                    prefix = path_str[:idx_blocks]
                    # O nome do pacote é o último diretório antes de 'extensions'
                    pkg_name = Path(prefix).parts[-1]
                    # Caminho relativo após 'extensions/blocks/'
                    relative_path = path_str[idx_blocks + len(blocks_marker):]
                    relative_path = relative_path.replace(".json", "")
                    block_type = relative_path.replace("/", ".")
                    block.type = f"{pkg_name}.extensions.blocks.{block_type}"
                except Exception as e:
                    logger.warning(f"Erro ao construir tipo completo para {file_name}: {e}")
                    block.type = data["type"]
            else:
                block.type = data["type"]
            block.language = data["language"]
            block.extension = data["extension"]
            block.help = data["help"]
            block.color = data["color"]
            block.label = data["label"]
            block.group = data["group"]

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
            for idx, port_data in enumerate(ports):
                from mosaicode.model.port import Port
                port = Port()
                conn_type = port_data.get("conn_type", "OUTPUT")
                if str(conn_type).upper() == "INPUT":
                    port.conn_type = "INPUT"
                else:
                    port.conn_type = "OUTPUT"
                port.name = port_data.get("name", "")
                port.label = port_data.get("label", "")
                port.type = port_data.get("type", "")
                port.color = port_data.get("color", "#FFFFFF")
                port.type_index = port_data.get("type_index", idx)
                port.hint = port_data.get("hint", "")
                block.ports.append(port)

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

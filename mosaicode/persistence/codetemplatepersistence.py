# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the CodeTemplatePersistence class.
"""
import ast
import logging
import inspect  # For module inspect
import pkgutil  # For dynamic package load
import json
from pathlib import Path
from typing import Optional, Dict, Any

from mosaicode.model.codetemplate import CodeTemplate
from mosaicode.persistence.persistence import Persistence

# Configure logging
logger = logging.getLogger(__name__)


class CodeTemplatePersistence:
    """
    This class contains methods related the CodeTemplatePersistence class.
    """

    # ----------------------------------------------------------------------
    @classmethod
    def load(cls, file_name: str) -> Optional[CodeTemplate]:
        """
        This method loads the code_template from JSON file.

        Args:
            file_name: Path to the JSON file

        Returns:
            CodeTemplate object or None if loading fails
        """
        # load the code_template
        file_path = Path(file_name)
        if not file_path.exists():
            return None
        if file_path.is_dir():
            return None

        code_template = CodeTemplate()
        data = ""

        try:
            with open(file_path, 'r') as data_file:
                data = json.load(data_file)

            if data["data"] != "CODE_TEMPLATE":
                return None

            code_template.version = data["version"]
            code_template.name = data["name"]
            code_template.type = data["type"]
            code_template.description = data["description"]
            code_template.language = data["language"]
            code_template.command = data["command"]

            props = data["properties"]
            for prop in props:
                code_template.properties.append(prop)

            codes = data["codes"]
            if codes:
                for key in codes:
                    code_template.codes[key] = codes[key]

            parts = data["code_parts"]
            for part in parts:
                code_template.code_parts.append(part.strip())
        except Exception as e:
            pass
        except IOError as e:
            pass

        if code_template.name == "":
            return None
        return code_template

    # ----------------------------------------------------------------------
    @classmethod
    def save(cls, code_template: CodeTemplate, path: str) -> bool:
        """
        This method save the code_template in user space.

        Args:
            code_template: The code template to save
            path: Directory path to save the template

        Returns:
            True if successful, False otherwise
        """

        x: Dict[str, Any] = {
            "source": "JSON",
            "data": "CODE_TEMPLATE",
            "version": code_template.version,
            'name': code_template.name,
            'type': code_template.type,
            'description': code_template.description,
            'language': code_template.language,
            'command': code_template.command,
            "code_parts": code_template.code_parts,
            "properties": [],
            "codes": {}
        }

        for key in code_template.properties:
            x["properties"].append(key)

        for key in code_template.codes:
            x["codes"][key] = code_template.codes[key]

        if not Persistence.create_dir(path):
            from mosaicode.system import System
            System.log("Problem creating dir to save Code templates")
            return False

        try:
            file_name = code_template.name
            output_path = Path(path) / f"{file_name}.json"
            with open(output_path, 'w') as data_file:
                json.dump(x, data_file, indent=4)
        except IOError as e:
            from mosaicode.system import System
            System.log(f"Problem saving Code template: {e}")
            return False
        return True

# ----------------------------------------------------------------------

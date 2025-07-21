# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the CodeTemplateControl class.
"""
import inspect  # For module inspect
from pathlib import Path
import logging
import pkgutil  # For dynamic package load

from mosaicode.model.codetemplate import CodeTemplate
from mosaicode.persistence.codetemplatepersistence import CodeTemplatePersistence


class CodeTemplateControl():
    """
    This class contains methods related the CodeTemplateControl class.
    """

    # ----------------------------------------------------------------------

    def __init__(self):
        pass

    # ----------------------------------------------------------------------
    @classmethod
    def load(cls, file_name):
        return CodeTemplatePersistence.load(file_name)

    # ----------------------------------------------------------------------
    @classmethod
    def add_code_template(cls, code_template):
        # save it
        from mosaicode.system import System as System
        System()
        # This would need to be integrated with the GUI to show a dialog
        # For now, we'll use a default location but log that user choice is preferred
        path = Path(System.get_user_dir()) / "extensions" / code_template.language / "codetemplates"
        System.log("Note: User should be prompted for save location in future versions")
        CodeTemplatePersistence.save(code_template, path)

    # ----------------------------------------------------------------------
    @classmethod
    def delete_code_template(cls, code_template_key):
        from mosaicode.system import System
        code_templates = System.get_code_templates()
        if code_template_key not in code_templates:
            System.log("Error: This code template does not exist")
            return False
        code_template = code_templates[code_template_key]
        if code_template.file is not None:
            Path(code_template.file).unlink(missing_ok=True)
        else:
            System.log("Error: This code template does not have a file.")            
        return code_template.file

    # ----------------------------------------------------------------------
    @classmethod
    def print_template(cls, code_template):
        """
        Print code template information.
        
        Args:
            code_template: CodeTemplate instance to print
        """
        logging.info(r"Code Template Type: {code_template.type}")
        logging.info(r"Code Template Label: {code_template.label}")
        logging.info(r"Code Template Language: {code_template.language}")
        logging.info(r"Code Template Extension: {code_template.extension}")
        logging.info(r"Code Template File: {code_template.file}")
        logging.info(r"Code Template Help: {code_template.help}")
        logging.info(r"Code Template Code: {code_template.code}")
        logging.info(r"---------------------")

# ----------------------------------------------------------------------

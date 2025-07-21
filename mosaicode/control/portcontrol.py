# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the PortControl class.
"""
import inspect  # For module inspect
from pathlib import Path
import logging
import pkgutil  # For dynamic package load

from mosaicode.model.port import Port
from mosaicode.persistence.portpersistence import PortPersistence


class PortControl():
    """
    This class contains methods related the PortControl class.
    """

    # ----------------------------------------------------------------------

    def __init__(self):
        pass

    # ----------------------------------------------------------------------
    @classmethod
    def load(cls, file_name):
        """
        This method loads the port from XML file.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        return PortPersistence.load(file_name)

    # ----------------------------------------------------------------------
    @classmethod
    def add_port(cls, port):
        from mosaicode.system import System as System
        System()
        # This would need to be integrated with the GUI to show a dialog
        # For now, we'll use a default location but log that user choice is preferred
        path = Path(System.get_user_dir()) / "extensions" / port.language / "ports"
        System.log("Note: User should be prompted for save location in future versions")
        PortPersistence.save(port, path)

    # ----------------------------------------------------------------------
    @classmethod
    def delete_port(cls, port_key):
        from mosaicode.system import System
        ports = System.get_ports()
        if port_key not in ports:
            return False
        port = ports[port_key]
        if port.file is not None:
            Path(port.file).unlink(missing_ok=True)
            return True
        else:
            return False

    # ----------------------------------------------------------------------
    @classmethod
    def print_port(cls, port):
        """
        Print port information.
        
        Args:
            port: Port instance to print
        """
        logging.info(r"Port Type: {port.type}")
        logging.info(r"Port Label: {port.label}")
        logging.info(r"Port Name: {port.name}")
        logging.info(r"Port Language: {port.language}")
        logging.info(r"Port File: {port.file}")
        logging.info(r"Port Color: {port.color}")
        logging.info(r"Port Multiple: {port.multiple}")
        logging.info(r"Port Required: {port.required}")
        logging.info(r"Port Max Conn: {port.max_conn}")
        logging.info(r"Port Min Conn: {port.min_conn}")
        logging.info(r"---------------------")
# ----------------------------------------------------------------------

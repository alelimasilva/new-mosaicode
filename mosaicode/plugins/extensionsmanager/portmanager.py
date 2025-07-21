#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# noqa: E402
"""
This module contains the PortManager class.
"""
import os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '3.0')
from gi.repository import Gtk
from gi.repository import GtkSource
from mosaicode.GUI.fields.stringfield import StringField
from mosaicode.GUI.fields.combofield import ComboField
from mosaicode.GUI.fields.colorfield import ColorField
from mosaicode.GUI.fields.commentfield import CommentField
from mosaicode.GUI.fields.codefield import CodeField
from mosaicode.GUI.fields.openfilefield import OpenFileField
from mosaicode.GUI.fieldtypes import *
from mosaicode.plugins.extensionsmanager.porteditor import PortEditor
from mosaicode.GUI.confirmdialog import ConfirmDialog
from mosaicode.GUI.buttonbar import ButtonBar
from mosaicode.system import *
from mosaicode.plugins.extensionsmanager.manager import Manager
import gettext

_ = gettext.gettext


class PortManager(Manager):
    """
    This class contains methods related the PortManager class
    """

    # ----------------------------------------------------------------------
    def __init__(self, main_window):
        from mosaicode.plugins.extensionsmanager.porteditor import PortEditor
        from mosaicode.model.port import Port
        from mosaicode.system import System
        def get_items():
            return System.get_ports()
        Manager.__init__(self, main_window, "Port Manager")
        self.element = Port()  # Para adicionar novo
        self.get_items = get_items
        self.editor = PortEditor
        self.update()
        self.show_all()
        self.show()

    # Sobrescrever __run_editor para salvar no arquivo correto
    def _PortManager__run_editor(self, element):
        from mosaicode.plugins.extensionsmanager.porteditor import PortEditor
        from mosaicode.persistence.portpersistence import PortPersistence
        from mosaicode.model.port import Port
        import os
        port = element if isinstance(element, Port) else Port()
        editor = PortEditor(self, port)
        result = editor.run()
        if result == 1:  # Gtk.ResponseType.OK
            port = editor.get_element()
            # Salvar no arquivo correto
            if port.type:
                from pathlib import Path
                project_root = Path(os.getcwd())
                found = False
                for ext_dir in project_root.glob("mosaicode-*/mosaicode_lib_*/extensions/ports"):
                    if ext_dir.is_dir():
                        file_path = ext_dir / f"{port.type}.json"
                        PortPersistence.save(port, str(file_path))
                        found = True
                        break
                if not found:
                    for ext_dir in project_root.glob("mosaicode-*/mosaicode_lib_*/extensions/ports"):
                        if ext_dir.is_dir():
                            file_path = ext_dir / f"{port.type}.json"
                            PortPersistence.save(port, str(file_path))
                            break
            self.update()
        editor.close()
        editor.destroy()

# ----------------------------------------------------------------------

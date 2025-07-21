# -*- coding: utf-8 -*-
"""
This module contains the PropertyBox class.
"""
import inspect  # For module inspect
import pkgutil  # For dynamic package load
import mosaicode.GUI.fields
import gi
import logging
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk  # type: ignore
from gi.repository import Gdk  # type: ignore
from mosaicode.GUI.fieldtypes import *
import gettext
from typing import Any, Optional, Dict, List, Callable
from mosaicode.model.blockmodel import BlockModel
from mosaicode.model.commentmodel import CommentModel
from mosaicode.model.diagrammodel import DiagramModel

_ = gettext.gettext


class PropertyBox(Gtk.VBox):
    """
    This class contains methods related the PropertyBox class.
    """

    # ----------------------------------------------------------------------

    def __init__(self, main_window: Any) -> None:
        """
        Initialize the PropertyBox.
        
        Args:
            main_window: The main window instance
        """
        Gtk.VBox.__init__(self, homogeneous=True, spacing=0)

        scrolled_window: Gtk.ScrolledWindow = Gtk.ScrolledWindow()
        scrolled_window.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        self.add(scrolled_window)

        self.vbox: Gtk.VBox = Gtk.VBox(homogeneous=False, spacing=0)
        scrolled_window.add(self.vbox)
        self.main_window: Any = main_window
        self.block: Optional[BlockModel] = None
        self.comment: Optional[CommentModel] = None
        self.diagram: Optional[DiagramModel] = None
        self.properties: Dict[str, Any] = {}
        self.vbox.set_property("border-width", 0)
        self.show_all()

    # ----------------------------------------------------------------------
    def set_diagram(self, diagram: DiagramModel) -> None:
        """
        This method set the property of the diagram.

        Parameters:
            * **diagram** (:class:`DiagramModel<mosaicode.model.diagrammodel>`)
        Returns:
            None
        """
        # First, remove all components
        for widget in self.vbox.get_children():
            self.vbox.remove(widget)
        self.diagram = diagram
        if diagram.code_template is None:
            data1: Dict[str, str] = {"label": _("Choose a Code Template"),
                    "name": "code_template",
                    "value": ""}
            field: Any = LabelField(data1, None)
            self.vbox.pack_start(field, False, False, 0)
            return
        self.__generate_fields(diagram.code_template.get_properties(),
                    self.notify_diagram)

    # ----------------------------------------------------------------------
    def set_comment(self, comment: CommentModel) -> None:
        """
        This method set the comment.

        Parameters:
            * **comment** (:class:`CommentModel<mosaicode.model.commentmodel>`)
        Returns:
            None
        """
        self.comment = comment
        self.__generate_fields(self.comment.get_properties(), self.notify_comment)

    # ----------------------------------------------------------------------
    def set_block(self, block: BlockModel) -> None:
        """
        This method set the block.

        Parameters:
            * **block** (:class:`BlockModel<mosaicode.model.blockmodel>`)
        Returns:
            None
        """
        logging.debug(r"PropertyBox.set_block chamado para bloco: {getattr(block, 'label', None)}")
        logging.debug(r"Propriedades recebidas: {getattr(block, 'properties', None)}")
        self.block = block
        self.__generate_fields(self.block.get_properties(), self.notify_block)

    # ----------------------------------------------------------------------
    def __recursive_search(self, container: Gtk.Container) -> None:
        """
        Recursively search for widgets in a container.
        
        Args:
            container: The container to search in
        """
        for widget in container.get_children():
            # If widget is a container, search inside it
            if isinstance(widget, Gtk.Container):
                self.__recursive_search(widget)
            # Once a component is found, search for it on the component list
            if widget.get_name() in self.properties:
                self.properties[widget.get_name()] = widget.get_value()

    # ----------------------------------------------------------------------
    def __generate_fields(self, props: List[Dict[str, Any]], callback: Callable[[Any, Any], None]) -> None:
        """
        Generate fields for properties.
        
        Args:
            props: List of property dictionaries
            callback: Callback function for property changes
        """
        logging.debug(r"PropertyBox.__generate_fields chamado com {len(props)} propriedades")
        logging.debug(r"Tipos de propriedades: {[prop.get('type', 'N/A') for prop in props]}")
        
        self.properties = {}
        for widget in self.vbox.get_children():
            self.vbox.remove(widget)
        
        for i, prop in enumerate(props):
            prop_type: str = prop.get("type", "String")
            prop_name: str = prop.get("name", "")
            prop_label: str = prop.get("label", prop_name)
            
            logging.debug(r"Processando propriedade {i+1}: {prop_label} ({prop_name}) - Tipo: {prop_type}")
            
            # Verificar se o tipo está mapeado
            if prop_type in component_list:
                logging.debug(r"[OK] Tipo {prop_type} encontrado em component_list")
                prop_field: Any = component_list[prop_type](prop, callback)
                self.properties[prop_name] = ""
                if prop_type == MOSAICODE_OPEN_FILE or prop_type == MOSAICODE_SAVE_FILE:
                    prop_field.set_parent_window(self.main_window)
                self.vbox.pack_start(prop_field, False, False, 0)
                logging.debug(r"[OK] Campo criado para {prop_name}")
            else:
                logging.debug(r"[ERRO] Tipo {prop_type} NÃO encontrado em component_list")
                logging.debug(r"Tipos disponíveis: {list(component_list.keys())}")
        
        if len(props) == 0:
            logging.debug(r"Nenhuma propriedade encontrada - criando campo 'No property is available'")
            data1: Dict[str, str] = {"label": "No property is available",
                "name": "",
                "value": ""}
            no_prop_field: Any = LabelField(data1, None)
            self.vbox.pack_start(no_prop_field, False, False, 0)
        
        logging.debug(r"PropertyBox.__generate_fields concluído - {len(self.vbox.get_children())} campos criados")

    # ----------------------------------------------------------------------
    def notify_block(self, widget: Optional[Any] = None, data: Optional[Any] = None) -> None:
        """
        This method notify modifications in propertybox
        """
        self.__recursive_search(self.vbox)
        if self.block:
            self.block.set_properties(self.properties)

    # ----------------------------------------------------------------------
    def notify_comment(self, widget: Optional[Any] = None, data: Optional[Any] = None) -> None:
        """
        This method notify modifications in propertybox
        """
        self.__recursive_search(self.vbox)
        if self.comment:
            self.comment.set_properties(self.properties)

    # ----------------------------------------------------------------------
    def notify_diagram(self, widget: Optional[Any] = None, data: Optional[Any] = None) -> None:
        """
        This method notify modifications in propertybox
        """
        self.__recursive_search(self.vbox)
        if self.diagram and self.diagram.code_template:
            self.diagram.code_template.set_properties(self.properties)

    # ----------------------------------------------------------------------
    def get_block(self) -> Optional[BlockModel]:
        """
        Get the current block.
        
        Returns:
            The current block or None
        """
        return self.block

    # ----------------------------------------------------------------------
    def get_comment(self) -> Optional[CommentModel]:
        """
        Get the current comment.
        
        Returns:
            The current comment or None
        """
        return self.comment

    # ----------------------------------------------------------------------
    def get_diagram(self) -> Optional[DiagramModel]:
        """
        Get the current diagram.
        
        Returns:
            The current diagram or None
        """
        return self.diagram

    # ----------------------------------------------------------------------
    def get_properties(self) -> Dict[str, Any]:
        """
        Get the current properties.
        
        Returns:
            Dictionary of current properties
        """
        return self.properties.copy()

    # ----------------------------------------------------------------------
    def clear(self) -> None:
        """
        Clear all fields and properties.
        """
        self.block = None
        self.comment = None
        self.diagram = None
        self.properties = {}
        
        # Remove all widgets
        for widget in self.vbox.get_children():
            self.vbox.remove(widget)

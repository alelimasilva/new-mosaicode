# -*- coding: utf-8 -*-
"""
This module contains the MainControl class.
"""
import gettext
import zipfile
import shutil
import signal
import subprocess
import datetime
import os
from copy import copy, deepcopy
from pathlib import Path
from threading import Event, Thread
from typing import List, Optional, Dict, Any, Union
import logging
import re
import urllib.request

import gi
# Importação direta e segura do Gtk
try:
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
except (ImportError, ValueError):
    raise ImportError('GTK 3.0 não está disponível. Instale o pacote python3-gi e libgtk-3-dev.')
from mosaicode.control.blockcontrol import BlockControl
from mosaicode.control.codegenerator import CodeGenerator
from mosaicode.control.codetemplatecontrol import CodeTemplateControl
from mosaicode.control.diagramcontrol import DiagramControl
from mosaicode.control.portcontrol import PortControl
from mosaicode.GUI.about import About
from mosaicode.GUI.block import Block
from mosaicode.GUI.codewindow import CodeWindow
from mosaicode.GUI.comment import Comment
from mosaicode.GUI.diagram import Diagram
from mosaicode.GUI.messagedialog import MessageDialog
from mosaicode.GUI.confirmdialog import ConfirmDialog
from mosaicode.GUI.savedialog import SaveDialog
from mosaicode.GUI.opendialog import OpenDialog
from mosaicode.GUI.preferencewindow import PreferenceWindow
from mosaicode.GUI.selectcodetemplate import SelectCodeTemplate
from mosaicode.model.blockmodel import BlockModel
from mosaicode.model.codetemplate import CodeTemplate
from mosaicode.model.port import Port
from mosaicode.model.commentmodel import CommentModel
from mosaicode.persistence.preferencespersistence import PreferencesPersistence
from mosaicode.persistence.portpersistence import PortPersistence
from mosaicode.persistence.blockpersistence import BlockPersistence
from mosaicode.persistence.codetemplatepersistence import CodeTemplatePersistence
from mosaicode.system import System as System
from mosaicode.utils.logger import get_logger

logger = get_logger(__name__)

_ = gettext.gettext


class MainControl:
    """
    This class contains methods related the MainControl class.
    """
    # ----------------------------------------------------------------------

    def __init__(self, main_window: Any) -> None:
        """
        Initialize MainControl.
        
        Args:
            main_window: The main window instance
        """
        self.main_window: Any = main_window
        # Clipboard is here because It must be possible to exchange data between diagrams
        self.clipboard: List[Any] = []
        self.threads: Dict[str, Any] = {}

    # ----------------------------------------------------------------------
    def init(self) -> None:
        """Initialize the main control."""
        logger.debug("[DEBUG] MainControl.init() - Iniciando inicialização")
        self.update_blocks()
        logger.debug("[DEBUG] MainControl.init() - update_blocks() concluído")
        self.main_window.menu.update_recent_files(
            System.get_preferences().recent_files)
        logger.debug("[DEBUG] MainControl.init() - update_recent_files() concluído")
        System.reload()
        logger.debug("[DEBUG] MainControl.init() - System.reload() concluído")
        self.main_window.menu.update_examples(System.get_examples())
        logger.debug("[DEBUG] MainControl.init() - Inicialização concluída")

    # ----------------------------------------------------------------------
    def update_blocks(self) -> None:
        """Update blocks in the system."""
        System.reload()
        blocks = System.get_blocks()
        self.main_window.menu.update_blocks(blocks)
        self.main_window.block_notebook.update_blocks(blocks)

    # ----------------------------------------------------------------------
    def new(self) -> None:
        """
        This method create a new the diagram file.
        """
        self.main_window.work_area.add_diagram(Diagram(self.main_window))

    # ----------------------------------------------------------------------
    def select_open(self) -> None:
        """
        This method open a selected file.
        """
        file_name: Optional[str] = OpenDialog(
                                "Open Diagram",
                                self.main_window,
                                filetype="mscd",
                                path=str(System.get_user_dir())
                                ).run()
        if file_name is None or file_name == "":
            return
        self.open(file_name)

    # ----------------------------------------------------------------------
    def open(self, file_name: str) -> None:
        """
        This method open a file.
        
        Args:
            file_name: Path to the file to open
        """
        diagram: Diagram = Diagram(self.main_window)
        self.main_window.work_area.add_diagram(diagram)
        if not DiagramControl(diagram).load(file_name):
            System.log("Problem Loading the Diagram")
        diagram.redraw()
        diagram.set_modified(False)

        self.set_recent_files(file_name)

    # ----------------------------------------------------------------------
    def close(self) -> None:
        """
        This method closes a tab on the work area.
        """
        self.main_window.work_area.close_tab()

    # ----------------------------------------------------------------------
    def save(self, save_as: bool = False) -> bool:
        """
        This method save the file.
        
        Args:
            save_as: Whether to show save as dialog
            
        Returns:
            True if save was successful, False otherwise
        """
        diagram: Optional[Diagram] = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False

        # If diagram already has a file name and it's not save_as, save directly
        if not save_as and diagram.file_name and diagram.file_name != "Untitled":
            success, message = DiagramControl(diagram).save()
            if not success:
                MessageDialog("Error", message, self.main_window).run()
            else:
                self.set_recent_files(diagram.file_name)
            return success

        # Show save dialog for new files or save_as
        while True:
            # Use current file name as default if available
            default_filename = diagram.file_name if diagram.file_name and diagram.file_name != "Untitled" else ""
            
            dialog: SaveDialog = SaveDialog(
                self.main_window,
                title=_("Save Diagram"),
                filename=default_filename,
                filetype="*.mscd")
            name: Optional[str] = dialog.run()
            if name is None:
                System.log("File not saved")
                return False

            if not name.endswith("mscd"):
                name = (("%s" + ".mscd") % name)

            if Path(name).exists():
                msg: str = _("File exists. Overwrite?")
                result: int = ConfirmDialog(msg, self.main_window).run()
                if result == Gtk.ResponseType.CANCEL:
                    continue

            diagram.file_name = name
            self.main_window.work_area.rename_diagram(diagram)
            break
        
        success: bool = False
        message: str = ""

        if diagram.file_name is not None:
            if len(diagram.file_name) > 0:
                success, message = DiagramControl(diagram).save()
                self.set_recent_files(diagram.file_name)

        if not success:
            MessageDialog("Error", message, self.main_window).run()
        
        return success

    # ----------------------------------------------------------------------
    def save_as(self) -> None:
        """
        This method save as.
        """
        self.save(save_as=True)

    # ----------------------------------------------------------------------
    def export_diagram(self) -> bool:
        """
        This method exports the diagram. Always asks user for save location.
        
        Returns:
            True if export was successful, False otherwise
        """
        diagram: Optional[Diagram] = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False

        # Always ask user for save location - no default paths
        while True:
            name: Optional[str] = SaveDialog(
                self.main_window,
                title=_("Export diagram as png"),
                filename="",  # No default path
                filetype="png").run()

            if name is None:
                return False
            if name.find(".png") == -1:
                name = name + ".png"
            if name is not None and Path(name).exists():
                msg: str = _("File exists. Overwrite?")
                result: int = ConfirmDialog(msg, self.main_window).run()
                if result == Gtk.ResponseType.OK:
                    break
            else:
                break

        success: bool
        message: str
        success, message = DiagramControl(diagram).export_png(name)

        if not success:
            MessageDialog("Error", message, self.main_window).run()
        
        return success

    # ----------------------------------------------------------------------
    def exit(self, widget: Optional[Any] = None, data: Optional[Any] = None) -> None:
        """
        This method close main window.
        """
        PreferencesPersistence.save(
            System.get_preferences(), System.get_user_dir())
        if self.main_window.work_area.close_tabs():
            Gtk.main_quit()
        else:
            return

    # ----------------------------------------------------------------------
    def set_recent_files(self, file_name: str) -> None:
        """
        Add file to recent files list.
        
        Args:
            file_name: Path to the file to add
        """
        if file_name in System.get_preferences().recent_files:
            System.get_preferences().recent_files.remove(file_name)
        System.get_preferences().recent_files.insert(0, file_name)
        if len(System.get_preferences().recent_files) > 10:
            System.get_preferences().recent_files.pop()
        self.main_window.menu.update_recent_files(
            System.get_preferences().recent_files)

        PreferencesPersistence.save(
            System.get_preferences(), System.get_user_dir())

    # ----------------------------------------------------------------------

    def get_clipboard(self) -> List[Any]:
        """
        This method return the clipboard.
        
        Returns:
            List of clipboard items
        """
        return self.clipboard

    # ----------------------------------------------------------------------
    def reset_clipboard(self) -> None:
        """
        This method clear the clipboard.
        """
        self.clipboard = []

    # ----------------------------------------------------------------------
    def preferences(self) -> None:
        """
        Open preferences window.
        """
        PreferenceWindow(self.main_window).run()

    # ----------------------------------------------------------------------
    def __get_code_generator(self, diagram: Diagram) -> Optional[CodeGenerator]:
        """
        Get code generator for diagram.
        
        Args:
            diagram: The diagram to generate code for
            
        Returns:
            CodeGenerator instance or None if not available
        """
        if diagram.language is None:
            message: str = "You shall not generate the code of an empty diagram!"
            MessageDialog("Error", message, self.main_window).run()
            return None

        if diagram.code_template is not None:
            return CodeGenerator(diagram)

        template_list: List[CodeTemplate] = []
        code_templates: Dict[str, CodeTemplate] = System.get_code_templates()

        for key in code_templates:
            if code_templates[key].language == diagram.language:
                template_list.append(code_templates[key])

        if len(template_list) == 0:
            message: str = "Generator not available for the language " + diagram.language + "."
            MessageDialog("Error", message, self.main_window).run()
            return None

        if len(template_list) == 1:
            diagram.code_template = deepcopy(template_list[0])
            return CodeGenerator(diagram)

        select: SelectCodeTemplate = SelectCodeTemplate(self.main_window, template_list)
        diagram.code_template = deepcopy(select.get_value())
        return CodeGenerator(diagram)

    # ----------------------------------------------------------------------
    def save_source(self, codes: Optional[Dict[str, str]] = None, generator: Optional[CodeGenerator] = None) -> bool:
        """
        This method saves the source codes. Always asks user for save location.
        
        Args:
            codes: Dictionary of code files to save
            generator: Code generator instance
            
        Returns:
            True if save was successful, False otherwise
        """
        diagram: Optional[Diagram] = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False

        # If it is not called from the run method
        if generator is None:
            generator = self.__get_code_generator(diagram)
            if generator is None:
                return False

        if codes is None:
            files: Dict[str, str] = generator.generate_code()
        else:
            files = codes
        
        # Ask user for save directory
        dialog: SaveDialog = SaveDialog(
            self.main_window,
            title=_("Select directory to save source code"),
            filename="",  # No default path
            filetype="*")
        save_dir: Optional[str] = dialog.run()
        if save_dir is None:
            System.log("Source code not saved")
            return False
        
        # Ensure it's a directory
        save_path = Path(save_dir)
        if not save_path.is_dir():
            save_path.mkdir(parents=True, exist_ok=True)
        
        # Save each file in the selected directory
        for key in files:
            file_name: str = str(save_path / key)
            logger.debug(f"[DEBUG] save_source - saving file: '{file_name}'")
            System.log("Saving Code to " + file_name)
            try:
                codeFile = open(file_name, 'w')
                codeFile.write(files[key])
                codeFile.close()
            except Exception as error:
                System.log("File or directory not found!")
                System.log(str(error))
        return True

    # ----------------------------------------------------------------------
    def save_source_only(self) -> bool:
        """
        This method saves the source codes without executing.
        
        Returns:
            True if save was successful, False otherwise
        """
        diagram: Optional[Diagram] = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False

        generator: Optional[CodeGenerator] = self.__get_code_generator(diagram)
        if generator is None:
            return False

        files: Dict[str, str] = generator.generate_code()
        
        # Ask user for save directory
        dialog: SaveDialog = SaveDialog(
            self.main_window,
            title=_("Select directory to save source code"),
            filename="",  # No default path
            filetype="*")
        save_dir: Optional[str] = dialog.run()
        if save_dir is None:
            System.log("Source code not saved")
            return False
        
        # Ensure it's a directory
        save_path = Path(save_dir)
        if not save_path.is_dir():
            save_path.mkdir(parents=True, exist_ok=True)
        
        # Save each file in the selected directory
        for key in files:
            file_name: str = str(save_path / key)
            logger.debug(f"[DEBUG] save_source_only - saving file: '{file_name}'")
            System.log("Saving Code to " + file_name)
            try:
                codeFile = open(file_name, 'w')
                codeFile.write(files[key])
                codeFile.close()
            except Exception as error:
                System.log("File or directory not found!")
                System.log(str(error))
                return False
        
        System.log("Source code saved successfully!")
        return True

    # ----------------------------------------------------------------------
    def execute_only(self) -> bool:
        System.log("[DEBUG] Entrou em execute_only() pelo botão Run da toolbar!")
        """
        This method executes the code without asking for save location.
        Uses temporary directory for execution.
        
        Returns:
            True if execution started successfully, False otherwise
        """
        diagram: Optional[Diagram] = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False

        generator: Optional[CodeGenerator] = self.__get_code_generator(diagram)
        if generator is None:
            return False

        files: Dict[str, str] = generator.generate_code()
        # Create temporary directory for execution
        import random
        random_number = ''.join(random.sample('0123456789', 5))
        temp_dir = System.DATA_DIR + "/code-gen/" + random_number
        os.mkdir(temp_dir)

        System.log(f"Using temporary directory for execution: {temp_dir}")
        
        # Save files to temporary directory
        for key in files:
            file_name: str = str(Path(temp_dir) / key)
            logger.debug(f"[DEBUG] execute_only - saving file: '{file_name}'")
            try:
                codeFile = open(file_name, 'w')
                codeFile.write(files[key])
                codeFile.close()
            except Exception as error:
                System.log("Error saving to temporary directory!")
                System.log(str(error))
                return False
        
        # Store original directory and set temporary directory
        original_dir = getattr(diagram, '_original_dir', None)
        diagram._original_dir = System.get_dir_name(diagram)
        
        # Temporarily modify the diagram's directory for execution
        # We'll use a custom attribute to store the temp dir
        diagram._temp_exec_dir = temp_dir
        
        # Garante que temp_dir termina com '/'
        temp_dir_slash = temp_dir if temp_dir.endswith(os.sep) else temp_dir + os.sep
        command: str = diagram.code_template.command
        if command is None:
            System.log("Error: No command template found for execution")
            return False
        command = command.replace("$dir_name$", temp_dir_slash)

        def __run_temp(self) -> None:
            try:
                process: subprocess.Popen = subprocess.Popen(command,
                                           cwd=temp_dir,
                                           shell=True,
                                           preexec_fn=os.setsid)
                self.threads[thread] = diagram, process
                self.main_window.toolbar.update_threads(self.threads)
                System.log(str(process.communicate()))
                del self.threads[thread]
                self.main_window.toolbar.update_threads(self.threads)
            finally:
                # Clean up temporary directory attribute
                if hasattr(diagram, '_temp_exec_dir'):
                    delattr(diagram, '_temp_exec_dir')

        thread: Thread = Thread(target=__run_temp, args=(self,))
        thread.start()

        System.log("Executing Code (temporary):\n" + command)

        return True

    # ----------------------------------------------------------------------
    def save_and_execute(self) -> bool:
        """
        This method saves the source codes and then executes them.
        
        Returns:
            True if save and execution were successful, False otherwise
        """
        # First save
        if not self.save_source_only():
            return False
        
        # Then execute using the saved directory
        diagram: Optional[Diagram] = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False

        dir_name = System.get_dir_name(diagram)
        dir_name_slash = dir_name if dir_name.endswith(os.sep) else dir_name + os.sep
        command: str = diagram.code_template.command
        if command is None:
            System.log("Error: No command template found for execution")
            return False
        command = command.replace("$dir_name$", dir_name_slash)

        def __run_saved(self) -> None:
            process: subprocess.Popen = subprocess.Popen(command,
                                       cwd=dir_name,
                                       shell=True,
                                       preexec_fn=os.setsid)
            self.threads[thread] = diagram, process
            self.main_window.toolbar.update_threads(self.threads)
            System.log(str(process.communicate()))
            del self.threads[thread]
            self.main_window.toolbar.update_threads(self.threads)

        System.log("Executing Code (saved):\n" + command)
        thread: Thread = Thread(target=__run_saved, args=(self,))
        thread.start()

        return True

    # ----------------------------------------------------------------------
    def view_source(self) -> bool:
        """
        This method view the source code.
        
        Returns:
            True if source was displayed, False otherwise
        """
        diagram: Optional[Diagram] = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False
        generator: Optional[CodeGenerator] = self.__get_code_generator(diagram)
        codes: Dict[str, str] = {}

        if generator is not None:
            codes = generator.generate_code()
        else:
            return False
        cw: CodeWindow = CodeWindow(self.main_window, codes)
        cw.run()
        cw.close()
        cw.destroy()
        return True
        

    # ----------------------------------------------------------------------
    def run(self, codes: Optional[Dict[str, str]] = None) -> bool:
        """
        This method runs the code.
        
        Args:
            codes: Dictionary of code files to run
            
        Returns:
            True if execution started successfully, False otherwise
        """
        diagram: Optional[Diagram] = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False

        generator: Optional[CodeGenerator] = self.__get_code_generator(diagram)
        if generator is None:
            return False

        self.save_source(codes=codes, generator=generator)

        command: str = diagram.code_template.command
        if command is None:
            System.log("Error: No command template found for execution")
            return False
        command = command.replace("$dir_name$", System.get_dir_name(diagram))

        def __run(self) -> None:
            process: subprocess.Popen = subprocess.Popen(command,
                                       cwd=System.get_dir_name(diagram),
                                       shell=True,
                                       preexec_fn=os.setsid)
            self.threads[thread] = diagram, process
            self.main_window.toolbar.update_threads(self.threads)
            System.log(str(process.communicate()))
            del self.threads[thread]
            self.main_window.toolbar.update_threads(self.threads)

        System.log("Executing Code:\n" + command)
        thread: Thread = Thread(target=__run, args=(self,))
        thread.start()

        return True

    # ----------------------------------------------------------------------
    def stop(self, widget: Any, process: Optional[subprocess.Popen]) -> None:
        """
        Stop a running process.
        
        Args:
            widget: The widget that triggered the stop
            process: The process to stop
        """
        if process is None:
            return
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)

    # ----------------------------------------------------------------------
    def about(self) -> None:
        """
        Show about dialog.
        """
        About(self.main_window).run()

    # ----------------------------------------------------------------------
    def search(self, query: str) -> None:
        """
        Search for blocks in the block notebook.
        """
        self.main_window.block_notebook.search(query)

    # ----------------------------------------------------------------------
    def set_block(self, block: BlockModel) -> None:
        """
        Set the selected block.
        
        Args:
            block: The block to select
        """
        self.main_window.property_box.set_block(block)

    # ----------------------------------------------------------------------
    def get_selected_block(self) -> Optional[BlockModel]:
        """
        Get the currently selected block.
        
        Returns:
            Selected block or None
        """
        return self.main_window.property_box.block

    # ----------------------------------------------------------------------
    def clear_console(self) -> None:
        """
        Clear the console output.
        """
        self.main_window.status.clear()

    # ----------------------------------------------------------------------
    def add_block(self, block: BlockModel) -> Optional[Block]:
        """
        Add a block to the current diagram.
        
        Args:
            block: The block to add
            
        Returns:
            The created Block instance or None if failed
        """
        diagram: Optional[Diagram] = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return None

        # Create a deep copy of the block to avoid conflicts with multiple instances
        from copy import deepcopy
        new_block: BlockModel = deepcopy(block)
        
        # Reset ID to ensure it gets a new unique ID
        new_block.id = -1

        # Se o diagrama não tem linguagem definida, usar a linguagem do bloco
        if diagram.language is None or diagram.language == 'None':
            diagram.language = new_block.language
            logging.warning(f'[DEBUG] MainControl: Definindo linguagem do diagrama para: {new_block.language}')
        
        # Se o diagrama já tem linguagem definida, verificar compatibilidade
        elif diagram.language != new_block.language:
            logging.warning(f'[DEBUG] MainControl: Incompatibilidade de linguagem: diagrama={diagram.language}, bloco={new_block.language}')
            System.log("Block language is different from diagram language.")
            return None

        # Assign new ID
        new_block.id = diagram.last_id
        diagram.last_id += 1

        # Use DiagramControl to add the block to the diagram
        diagram_control: DiagramControl = DiagramControl(diagram)
        if not diagram_control.add_block(new_block):
            return None

        # Create the Block widget
        block_widget: Block = Block(diagram, new_block)
        block_widget.is_selected = True
        diagram.redraw()
        logging.warning(f'[DEBUG] MainControl: Bloco criado com sucesso: {new_block.type} (ID: {new_block.id})')
        return block_widget

    # ----------------------------------------------------------------------
    def add_comment(self, comment: Optional[CommentModel] = None) -> Optional[Comment]:
        """
        Add a comment to the current diagram.
        
        Args:
            comment: The comment model to add
            
        Returns:
            The created Comment instance or None if failed
        """
        diagram: Optional[Diagram] = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return None

        new_comment: Comment = Comment(diagram, comment)
        diagram.add_comment(new_comment)
        if comment is None:
            new_comment.is_selected = True
            diagram.show_comment_property(new_comment)
        diagram.redraw()
        return new_comment

    # ----------------------------------------------------------------------
    def select_all(self) -> None:
        """
        Select all elements in the current diagram.
        """
        diagram: Optional[Diagram] = self.main_window.work_area.get_current_diagram()
        if diagram is not None:
            diagram.select_all()

    # ----------------------------------------------------------------------
    def cut(self) -> None:
        # logging.warning('[DEBUG] MainControl.cut chamado')
        diagram: Optional[Diagram] = self.main_window.work_area.get_current_diagram()
        if diagram is not None:
            logging.warning(f'[DEBUG] Diagrama atual: {diagram}')
            diagram.cut()
        else:
            logging.warning('[DEBUG] Nenhum diagrama atual encontrado em cut')

    # ----------------------------------------------------------------------
    def copy(self) -> None:
        # logging.warning('[DEBUG] MainControl.copy chamado')
        diagram: Optional[Diagram] = self.main_window.work_area.get_current_diagram()
        if diagram is not None:
            logging.warning(f'[DEBUG] Diagrama atual: {diagram}')
            diagram.copy()
        else:
            logging.warning('[DEBUG] Nenhum diagrama atual encontrado em copy')

    # ----------------------------------------------------------------------
    def paste(self) -> None:
        # logging.warning('[DEBUG] MainControl.paste chamado')
        diagram: Optional[Diagram] = self.main_window.work_area.get_current_diagram()
        if diagram is not None:
            logging.warning(f'[DEBUG] Diagrama atual: {diagram}')
            diagram.paste()
        else:
            logging.warning('[DEBUG] Nenhum diagrama atual encontrado em paste')

    # ----------------------------------------------------------------------
    def delete(self) -> None:
        """
        Delete selected elements.
        """
        diagram: Optional[Diagram] = self.main_window.work_area.get_current_diagram()
        if diagram is not None:
            diagram.delete()

    # ----------------------------------------------------------------------
    def zoom_in(self) -> None:
        """
        Zoom in on the current diagram.
        """
        diagram: Optional[Diagram] = self.main_window.work_area.get_current_diagram()
        if diagram is not None:
            diagram.zoom_in()

    # ----------------------------------------------------------------------
    def zoom_out(self) -> None:
        """
        Zoom out on the current diagram.
        """
        diagram: Optional[Diagram] = self.main_window.work_area.get_current_diagram()
        if diagram is not None:
            diagram.zoom_out()

    # ----------------------------------------------------------------------
    def zoom_normal(self) -> None:
        """
        Reset zoom to normal on the current diagram.
        """
        diagram: Optional[Diagram] = self.main_window.work_area.get_current_diagram()
        if diagram is not None:
            diagram.zoom_normal()

    # ----------------------------------------------------------------------
    def undo(self) -> None:
        logging.warning('[DEBUG] MainControl.undo chamado')
        diagram: Optional[Diagram] = self.main_window.work_area.get_current_diagram()
        if diagram is not None:
            logging.warning(f'[DEBUG] Diagrama atual: {diagram}')
            diagram.undo()
        else:
            logging.warning('[DEBUG] Nenhum diagrama atual encontrado em undo')

    # ----------------------------------------------------------------------
    def redo(self) -> None:
        logging.warning('[DEBUG] MainControl.redo chamado')
        diagram: Optional[Diagram] = self.main_window.work_area.get_current_diagram()
        if diagram is not None:
            logging.warning(f'[DEBUG] Diagrama atual: {diagram}')
            diagram.redo()
        else:
            logging.warning('[DEBUG] Nenhum diagrama atual encontrado em redo')

    # ----------------------------------------------------------------------
    def align_top(self) -> None:
        logging.warning('[DEBUG] MainControl.align_top chamado')
        diagram: Optional[Diagram] = self.main_window.work_area.get_current_diagram()
        if diagram is not None:
            logging.warning(f'[DEBUG] Diagrama atual: {diagram}')
            diagram.align_top()
        else:
            logging.warning('[DEBUG] Nenhum diagrama atual encontrado em align_top')

    # ----------------------------------------------------------------------
    def align_bottom(self) -> None:
        logging.warning('[DEBUG] MainControl.align_bottom chamado')
        diagram: Optional[Diagram] = self.main_window.work_area.get_current_diagram()
        if diagram is not None:
            logging.warning(f'[DEBUG] Diagrama atual: {diagram}')
            diagram.align_bottom()
        else:
            logging.warning('[DEBUG] Nenhum diagrama atual encontrado em align_bottom')

    # ----------------------------------------------------------------------
    def align_left(self) -> None:
        logging.warning('[DEBUG] MainControl.align_left chamado')
        diagram: Optional[Diagram] = self.main_window.work_area.get_current_diagram()
        if diagram is not None:
            logging.warning(f'[DEBUG] Diagrama atual: {diagram}')
            diagram.align_left()
        else:
            logging.warning('[DEBUG] Nenhum diagrama atual encontrado em align_left')

    # ----------------------------------------------------------------------
    def align_right(self) -> None:
        logging.warning('[DEBUG] MainControl.align_right chamado')
        diagram: Optional[Diagram] = self.main_window.work_area.get_current_diagram()
        if diagram is not None:
            logging.warning(f'[DEBUG] Diagrama atual: {diagram}')
            diagram.align_right()
        else:
            logging.warning('[DEBUG] Nenhum diagrama atual encontrado em align_right')

    # ----------------------------------------------------------------------
    def collapse_all(self) -> None:
        """
        Collapse all blocks in the current diagram.
        """
        diagram: Optional[Diagram] = self.main_window.work_area.get_current_diagram()
        if diagram is not None:
            diagram.collapse_all()

    # ----------------------------------------------------------------------
    def uncollapse_all(self) -> None:
        """
        Uncollapse all blocks in the current diagram.
        """
        diagram: Optional[Diagram] = self.main_window.work_area.get_current_diagram()
        if diagram is not None:
            diagram.uncollapse_all()

    # ----------------------------------------------------------------------
    def redraw(self, show_grid: bool) -> None:
        """
        Redraw the current diagram.
        
        Args:
            show_grid: Whether to show the grid
        """
        diagram: Optional[Diagram] = self.main_window.work_area.get_current_diagram()
        if diagram is not None:
            diagram.redraw()

    # ----------------------------------------------------------------------
    def toggle_grid(self, event: Any = None) -> None:
        """
        Alterna a visibilidade da grade.
        Args:
            event: O evento que disparou a alternância (opcional)
        """
        diagram: Optional[Diagram] = self.main_window.work_area.get_current_diagram()
        if diagram is not None:
            diagram.toggle_grid(event)

    # ----------------------------------------------------------------------
    def add_extension(self, element: Any) -> None:
        """
        Add an extension to the system.
        
        Args:
            element: The extension element to add
        """
        try:
            if isinstance(element, BlockModel):
                BlockControl.add_new_block(element)
            elif isinstance(element, Port):
                PortControl.add_port(element)
            elif isinstance(element, CodeTemplate):
                CodeTemplateControl.add_code_template(element)
            else:
                logger.warning(f"Unknown extension type: {type(element)}")
                return
            
            # Reload system to include new extension
            System.reload()
            self.update_blocks()
            logger.info(f"Extension added successfully: {element.type if hasattr(element, 'type') else 'unknown'}")
        except Exception as e:
            logger.error(f"Error adding extension: {e}")
            if hasattr(self.main_window, 'get_window') and self.main_window.get_window() is not None:
                MessageDialog("Error", f"Error adding extension: {str(e)}", self.main_window).run()

    # ----------------------------------------------------------------------
    def delete_extension(self, element_name: str, element_type: Any) -> None:
        """
        Delete an extension from the system.
        
        Args:
            element_name: Name/type of the extension to delete
            element_type: Type of the extension (BlockModel, Port, or CodeTemplate)
        """
        try:
            if element_type == BlockModel:
                success = BlockControl.delete_block(element_name)
            elif element_type == Port:
                success = PortControl.delete_port(element_name)
            elif element_type == CodeTemplate:
                success = CodeTemplateControl.delete_code_template(element_name)
            else:
                logger.warning(f"Unknown extension type: {element_type}")
                return
            
            if success:
                # Reload system to reflect changes
                System.reload()
                self.update_blocks()
                logger.info(f"Extension deleted successfully: {element_name}")
            else:
                logger.warning(f"Failed to delete extension: {element_name}")
                if hasattr(self.main_window, 'get_window') and self.main_window.get_window() is not None:
                    MessageDialog("Warning", f"Failed to delete extension: {element_name}", self.main_window).run()
        except Exception as e:
            logger.error(f"Error deleting extension: {e}")
            if hasattr(self.main_window, 'get_window') and self.main_window.get_window() is not None:
                MessageDialog("Error", f"Error deleting extension: {str(e)}", self.main_window).run()

    # ----------------------------------------------------------------------
    def export_extensions(self) -> bool:
        """
        Export all extensions to a zip file. Always asks user for save location.
        
        Returns:
            True if export was successful, False otherwise
        """
        from mosaicode.system import System as System
        System()

        # Ask user for save location
        dialog: SaveDialog = SaveDialog(
            self.main_window,
            title=_("Select directory to export extensions"),
            filename="",  # No default path
            filetype="*")
        save_dir: Optional[str] = dialog.run()
        if save_dir is None:
            System.log("Extensions not exported")
            return False
        
        # Ensure it's a directory
        save_path = Path(save_dir)
        if not save_path.is_dir():
            save_path.mkdir(parents=True, exist_ok=True)

        result: bool = True
        folder: str = "extension-" + datetime.datetime.now().strftime("%Y-%m-%d")
        folder_path: Path = save_path / folder

        try:
            folder_path.mkdir(parents=True, exist_ok=True)

            # Export ports
            ports: Dict[str, Port] = System.get_ports()
            for key in ports:
                port = ports[key]
                port_dir = folder_path / port.language / 'ports'
                port_dir.mkdir(parents=True, exist_ok=True)
                result = result and PortPersistence.save(port, str(port_dir))

            # Export Blocks
            blocks: Dict[str, BlockModel] = System.get_blocks()
            for key in blocks:
                block = blocks[key]
                block_dir = folder_path / block.language / 'blocks' / block.extension / block.group
                block_dir.mkdir(parents=True, exist_ok=True)
                result = result and BlockPersistence.save(block, str(block_dir))

            # Export Code Templates
            code_templates: Dict[str, CodeTemplate] = System.get_code_templates()
            for key in code_templates:
                template = code_templates[key]
                template_dir = folder_path / template.language / 'codetemplates'
                template_dir.mkdir(parents=True, exist_ok=True)
                result = result and CodeTemplatePersistence.save(template, str(template_dir))

            # Export examples - only if they exist in the user extensions directory
            user_extensions_path: Path = Path(System.get_user_dir()) / "extensions"
            examples: List[str] = System.get_examples()
            for example in examples:
                example_path = Path(example)
                if example_path.exists():
                    try:
                        relpath = example_path.relative_to(user_extensions_path)
                        example_dest_path = folder_path / relpath
                        example_dest_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(example_path, example_dest_path)
                    except ValueError:
                        logger.debug(f"Skipping example not in user extensions: {example}")
                        continue

            # Create a zip file
            zip_path: Path = save_path / f"{folder}.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for file_path in folder_path.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(folder_path)
                        zip_file.write(file_path, arcname)

            shutil.rmtree(folder_path)

            if hasattr(self.main_window, 'get_window') and self.main_window.get_window() is not None:
                if result:
                    MessageDialog(
                            "Success",
                             f"File {folder}.zip created successfully in {save_path}!",
                             self.main_window).run()
                else:
                    MessageDialog(
                            "Error",
                            "Could not export extension",
                            self.main_window).run()
            else:
                if result:
                    logger.info(f"Export successful: {folder}.zip created in {save_path}")
                else:
                    logger.error("Export failed")
            return result

        except Exception as e:
            logger.error(f"Error during export: {e}")
            if folder_path.exists():
                shutil.rmtree(folder_path)
            if hasattr(self.main_window, 'get_window') and self.main_window.get_window() is not None:
                MessageDialog(
                        "Error",
                        f"Error exporting extensions: {str(e)}",
                        self.main_window).run()
            else:
                logger.error(f"Error exporting extensions: {str(e)}")
            return False

    # ----------------------------------------------------------------------
    def import_extensions(self) -> None:
        """
        Import extensions from the server, permitindo seleção múltipla visual.
        """
        import urllib.request
        import urllib.error
        import zipfile
        import os
        from mosaicode.GUI.extensionimportdialog import ExtensionImportDialog
        from mosaicode.system import System
        
        if Gtk is None:
            logging.info(r"[ERRO] GTK não está disponível.")
            return

        # Buscar lista de extensões disponíveis
        extensions = self.fetch_available_extensions()
        if not extensions:
            if hasattr(self.main_window, 'get_window') and self.main_window.get_window() is not None:
                MessageDialog(
                    "Erro",
                    "Não foi possível acessar o servidor de extensões ou não há extensões disponíveis."
                )
            else:
                logging.info(r"[ERRO] Não foi possível acessar o servidor de extensões ou não há extensões disponíveis.")
            return

        # Corrigir parent: garantir Gtk.Window ou None
        parent = self.main_window if hasattr(self.main_window, 'props') and hasattr(self.main_window, 'get_title') else None
        dialog = ExtensionImportDialog(parent, extensions)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            selected_files = dialog.get_selected_files()
            if selected_files:
                self._download_and_install_extensions(selected_files, extensions)
        dialog.destroy()

    # ----------------------------------------------------------------------
    def update_all(self) -> None:
        """
        Update all diagrams in the work area.
        """
        for diagram in self.main_window.work_area.get_diagrams():
            diagram.update()

    def fetch_available_extensions(self) -> List[Dict[str, str]]:
        """
        Busca e faz o parsing do índice do servidor de extensões, retornando uma lista de arquivos zip (nome, data, tamanho).
        Retorna uma lista de dicionários: [{"name": ..., "date": ..., "size": ...}, ...]
        """
        from mosaicode.system import System
        extension_server_url = System.get_system_value("extension_server_url", "https://alice.ufsj.edu.br/mosaicode/extensions/")
        index_url = extension_server_url
        try:
            with urllib.request.urlopen(index_url) as response:
                html = response.read().decode('utf-8')
            logging.debug(f"HTML baixado do índice: {html[:500]}")
        except Exception as e:
            logger.error(f"Erro ao acessar o índice do servidor de extensões: {e}")
            return []

        # Regex para o formato real do Apache Directory Listing
        pattern = re.compile(r'<a href="([^"]+\.zip)">[^<]+</a></td><td align="right">([\d\-: ]+)</td><td align="right">([\dKMG]+)</td>', re.IGNORECASE)
        matches = pattern.findall(html)
        logging.debug(r"Matches encontrados: {matches}")

        extensions = []
        for name, date, size in matches:
            if name.startswith('.'):
                continue
            extensions.append({"name": name, "date": date.strip(), "size": size.strip()})
        logging.debug(r"Lista final de extensões extraídas: {extensions}")
        return extensions

    def _download_and_install_extensions(self, selected_files, extensions):
        import urllib.request
        import zipfile
        import os
        from mosaicode.system import System
        from pathlib import Path
        
        base_dir: Path = Path.cwd()
        extension_server_url = System.get_system_value("extension_server_url", "https://alice.ufsj.edu.br/mosaicode/extensions/")
        success_count = 0
        error_count = 0
        for file_name in selected_files:
            try:
                file_url = extension_server_url + file_name
                file_path: Path = base_dir / file_name
                logging.info(r"[INFO] Baixando {file_name}...")
                urllib.request.urlretrieve(file_url, file_path)
                destination: Path = base_dir / "extensions"
                destination.mkdir(parents=True, exist_ok=True)
                with zipfile.ZipFile(file_path, 'r') as zip_file:
                    zip_file.extractall(destination)
                file_path.unlink(missing_ok=True)
                success_count += 1
                logging.info(r"[INFO] Extensão importada: {file_name}")
            except Exception as e:
                logging.info(r"[ERRO] Erro ao importar {file_name}: {e}")
                error_count += 1
        System.reload()
        # Mensagem final
        if hasattr(self.main_window, 'get_window') and self.main_window.get_window() is not None:
            if success_count > 0:
                msg = f"{success_count} extensão(ões) importada(s) com sucesso."
                if error_count > 0:
                    msg += f"\n{error_count} falha(s) ao importar."
                MessageDialog("Sucesso", msg, self.main_window).run()
            else:
                MessageDialog("Erro", f"Falha ao importar extensões. {error_count} erro(s).", self.main_window).run()
        else:
            if success_count > 0:
                logging.info(r"[INFO] {success_count} extensão(ões) importada(s) com sucesso.")
            if error_count > 0:
                logging.info(r"[ERRO] {error_count} falha(s) ao importar extensões.")

# ----------------------------------------------------------------------

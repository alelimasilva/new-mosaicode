# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the DiagramControl class.
"""
import os
import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
from copy import deepcopy
from copy import copy
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import logging

from mosaicode.system import System as System
from mosaicode.persistence.diagrampersistence import DiagramPersistence
from mosaicode.GUI.comment import Comment
from mosaicode.model.commentmodel import CommentModel
from mosaicode.model.blockmodel import BlockModel
from mosaicode.model.connectionmodel import ConnectionModel


class DiagramControl:
    """
    This class contains methods related the DiagramControl class.
    """

    # ----------------------------------------------------------------------
    def __init__(self, diagram: Any) -> None:
        """
        Initialize DiagramControl.
        
        Args:
            diagram: The diagram to control
        """
        self.diagram: Any = diagram

    # ----------------------------------------------------------------------
    def add_block(self, block: BlockModel) -> bool:
        """
        This method add a block in the diagram.

        Args:
            block: The block to add
            
        Returns:
            True if block was added successfully, False otherwise
        """
        # Se o diagrama não tem linguagem definida, usar a linguagem do bloco
        if self.diagram.language is None or self.diagram.language == 'None':
            self.diagram.language = block.language
            # logging.warning(f'[DEBUG] Definindo linguagem do diagrama para: {block.language}')
        
        # Se o diagrama já tem linguagem definida, verificar compatibilidade
        elif self.diagram.language != block.language:
            # logging.warning(f'[DEBUG] Incompatibilidade de linguagem: diagrama={self.diagram.language}, bloco={block.language}')
            System.log("Block language is different from diagram language.")
            return False

        self.do("Add Block")
        self.diagram.last_id = max(int(self.diagram.last_id), int(block.id))
        if block.id < 0:
            block.id = self.diagram.last_id
        self.diagram.last_id += 1
        self.diagram.blocks[block.id] = block
        # logging.warning(f'[DEBUG] Bloco adicionado com sucesso: {block.type} (ID: {block.id})')
        return True

    # ---------------------------------------------------------------------
    def paste(self) -> None:
        logging.warning('[DEBUG] DiagramControl.paste chamado')
        replace: Dict[int, BlockModel] = {}
        self.diagram.deselect_all()
        # interact into blocks, add blocks and change their id
        clipboard: List[Any] = self.diagram.main_window.main_control.get_clipboard()
        logging.warning(f'[DEBUG] Clipboard antes do paste: {clipboard}')
        logging.warning(f'[DEBUG] Blocos antes do paste: {list(self.diagram.blocks.keys())}')

        for widget in clipboard:
            if not isinstance(widget, BlockModel):
                continue
            # Criar um novo BlockModel preservando todos os atributos do widget original
            block: BlockModel = BlockModel()
            # Copiar todos os atributos relevantes do widget original
            for field_name in widget.__dataclass_fields__:
                if field_name not in ['id', 'x', 'y']:  # Não copiar id e posição
                    setattr(block, field_name, getattr(widget, field_name))
            
            logging.warning(f'[DEBUG] Bloco para paste - language: {block.language}, type: {block.type}')
            block.x = widget.x + 20
            block.y = widget.y + 20
            block.id = -1
            block = self.diagram.main_window.main_control.add_block(block)
            if block is None:
                return
            replace[widget.id] = block

        # interact into connections changing block ids
        for widget in clipboard:
            if not isinstance(widget, ConnectionModel):
                continue
            # if a connector is copied without blocks
            if (widget.output is None or widget.input is None or 
                widget.output.id not in replace or widget.input.id not in replace):
                continue
            output_block: BlockModel = replace[widget.output.id]
            output_port: Any = widget.output_port
            input_block: BlockModel = replace[widget.input.id]
            input_port: Any = widget.input_port
            self.diagram.start_connection(output_block, output_port)
            self.diagram.curr_connector.is_selected = True
            self.diagram.end_connection(input_block, input_port)

        for widget in clipboard:
            if not isinstance(widget, CommentModel):
                continue
            comment: CommentModel = CommentModel()
            # Copiar atributos do comentário original
            for field_name in widget.__dataclass_fields__:
                if field_name not in ['id', 'x', 'y']:  # Não copiar id e posição
                    setattr(comment, field_name, getattr(widget, field_name))
            comment.x = widget.x + 20
            comment.y = widget.y + 20
            self.diagram.main_window.main_control.add_comment(comment)


        self.diagram.update_flows()
        self.diagram.redraw()
        logging.warning(f'[DEBUG] Blocos após paste: {list(self.diagram.blocks.keys())}')
        logging.warning('[DEBUG] DiagramControl.paste finalizado')

    # ---------------------------------------------------------------------
    def copy(self) -> None:
        logging.warning('[DEBUG] DiagramControl.copy chamado')
        mc: Any = self.diagram.main_window.main_control
        mc.reset_clipboard()
        for key in self.diagram.blocks:
            if not self.diagram.blocks[key].is_selected:
                continue
            mc.get_clipboard().append(self.diagram.blocks[key])
        for conn in self.diagram.connectors:
            if not conn.is_selected:
                continue
            mc.get_clipboard().append(conn)
        for comment in self.diagram.comments:
            if not comment.is_selected:
                continue
            mc.get_clipboard().append(comment)
        logging.warning(f'[DEBUG] Clipboard após copy: {mc.get_clipboard()}')
        logging.warning(f'[DEBUG] Blocos selecionados para copy: {[key for key in self.diagram.blocks if self.diagram.blocks[key].is_selected]}')

    # ---------------------------------------------------------------------
    def cut(self) -> None:
        logging.warning('[DEBUG] DiagramControl.cut chamado')
        self.do("Cut")
        self.copy()
        self.delete()
        logging.warning(f'[DEBUG] Clipboard após cut: {self.diagram.main_window.main_control.get_clipboard()}')
        logging.warning(f'[DEBUG] Blocos após cut: {list(self.diagram.blocks.keys())}')
        logging.warning('[DEBUG] DiagramControl.cut finalizado')

    # ---------------------------------------------------------------------
    def delete(self) -> None:
        """
        This method delete a block or connection.
        """
        self.do("Delete")
        for key in self.diagram.blocks.copy():
            if not self.diagram.blocks[key].is_selected:
                continue
            del self.diagram.blocks[key]
        for con in self.diagram.connectors:
            if not con.is_selected:
                continue
            if con not in self.diagram.connectors:
                continue
            self.diagram.connectors.remove(con)
        for comment in self.diagram.comments:
            if not comment.is_selected:
                continue
            self.diagram.comments.remove(comment)

        self.diagram.deselect_all()
        self.diagram.redraw()

    # ----------------------------------------------------------------------
    def add_comment(self, comment: Optional[CommentModel] = None) -> Optional[Comment]:
        """
        This method add a comment in the diagram.

        Args:
            comment: The comment model to add
            
        Returns:
            The created Comment instance or None if failed
        """
        self.do("Add Comment")
        new_comment: Comment = Comment(self.diagram, comment)
        self.diagram.comments.append(new_comment)
        if comment is None:
            new_comment.is_selected = True
            self.diagram.show_comment_property(new_comment)
        self.diagram.redraw()
        return new_comment

    # ----------------------------------------------------------------------
    def add_connection(self, connection: ConnectionModel) -> bool:
        """
        This method adds a connection to the diagram.

        Args:
            connection: The connection to add
            
        Returns:
            True if connection was added successfully
        """
        self.do("Add Connection")
        self.diagram.connectors.append(connection)
        return True

    # ----------------------------------------------------------------------
    def collapse_all(self, status: bool) -> bool:
        """
        This method Collapses all the blocks in a diagram

        Args:
            status: Whether to collapse (True) or uncollapse (False)
            
        Returns:
            True if operation was successful
        """
        for key in self.diagram.blocks:
            self.diagram.blocks[key].is_collapsed = status
        self.diagram.redraw()
        return True

    # ----------------------------------------------------------------------
    def align(self, alignment: str) -> None:
        logging.warning(f'[DEBUG] DiagramControl.align chamado com alignment={alignment}')
        top: int = self.diagram.main_window.get_size()[1]
        bottom: int = 0
        left: int = self.diagram.main_window.get_size()[0]
        right: int = 0
        selected = [b for b in self.diagram.blocks.values() if getattr(b, 'is_selected', False)]
        logging.warning(f'[DEBUG] Blocos selecionados: {len(selected)}')
        for key in self.diagram.blocks:
            if not self.diagram.blocks[key].is_selected:
                continue
            x, y = self.diagram.blocks[key].get_position()
            if top > y: top = y
            if bottom < y: bottom = y
            if left > x: left = x
            if right < x: right = x
        for key in self.diagram.blocks:
            if not self.diagram.blocks[key].is_selected:
                continue
            x, y = self.diagram.blocks[key].get_position()
            if alignment == "BOTTOM":
                self.diagram.blocks[key].move(0, bottom - y)
            if alignment == "TOP":
                self.diagram.blocks[key].move(0, top - y)
            if alignment == "LEFT":
                self.diagram.blocks[key].move(left - x, 0)
            if alignment == "RIGHT":
                self.diagram.blocks[key].move(right - x, 0)
        self.diagram.update_flows()
        self.diagram.redraw()
        logging.warning('[DEBUG] DiagramControl.align finalizado')

    # ----------------------------------------------------------------------
    def set_show_grid(self, status: Optional[bool]) -> None:
        """
        Set grid visibility.
        
        Args:
            status: Whether to show grid
        """
        if status is not None:
            self.diagram.show_grid = status

    # ---------------------------------------------------------------------
    def do(self, new_msg: str) -> None:
        """
        This method do something
        
        Args:
            new_msg: Action message
        """
        # Salvar o estado ANTES da ação para poder desfazer
        serialized_blocks = {}
        for block_id, block in self.diagram.blocks.items():
            # Criar uma cópia serializada do bloco
            serialized_block = {
                'id': block.id,
                'type': block.type,
                'language': block.language,
                'x': block.x,
                'y': block.y,
                'label': block.label,
                'color': block.color,
                'group': block.group,
                'help': block.help,
                'version': block.version,
                'extension': block.extension,
                'file': block.file,
                'is_collapsed': block.is_collapsed,
                'ports': block.ports.copy() if hasattr(block, 'ports') else [],
                'properties': block.properties.copy() if hasattr(block, 'properties') else [],
                'codes': block.codes.copy() if hasattr(block, 'codes') else {},
                'gen_codes': block.gen_codes.copy() if hasattr(block, 'gen_codes') else {},
                'weight': block.weight,
                'connections': block.connections.copy() if hasattr(block, 'connections') else [],
                'maxIO': block.maxIO
            }
            serialized_blocks[block_id] = serialized_block
        
        # Serializar conectores e comentários
        serialized_connectors = []
        for conn in self.diagram.connectors:
            serialized_conn = {
                'output': {'id': conn.output.id} if hasattr(conn, 'output') and conn.output else None,
                'input': {'id': conn.input.id} if hasattr(conn, 'input') and conn.input else None,
                'output_port': conn.output_port,
                'input_port': conn.input_port
            }
            serialized_connectors.append(serialized_conn)
        
        serialized_comments = []
        for comment in self.diagram.comments:
            serialized_comment = {
                'id': comment.id,
                'x': comment.x,
                'y': comment.y,
                'text': comment.text,
                'color': comment.color
            }
            serialized_comments.append(serialized_comment)
        
        action: Tuple[Dict[int, Any], List[Any], List[Any], str] = (serialized_blocks,    #0
                  serialized_connectors,#1
                  serialized_comments,  #2
                  new_msg)              #3
        self.diagram.undo_stack.append(action)
        self.diagram.set_modified(True)
        logging.warning(f'[DEBUG] do() - Ação salva: {new_msg}, blocos: {list(serialized_blocks.keys())}, undo_stack: {len(self.diagram.undo_stack)}')

    # ---------------------------------------------------------------------
    def undo(self) -> None:
        logging.warning('[DEBUG] DiagramControl.undo chamado')
        if len(self.diagram.undo_stack) < 1:
            logging.warning('[DEBUG] undo_stack vazio')
            return
        self.diagram.set_modified(True)
        
        # Salvar o estado atual no redo_stack antes de restaurar
        current_state = self._serialize_current_state("Current State")
        self.diagram.redo_stack.append(current_state)
        
        action: Tuple[Dict[int, Any], List[Any], List[Any], str] = self.diagram.undo_stack.pop()
        
        logging.warning(f'[DEBUG] undo() - Blocos antes: {list(self.diagram.blocks.keys())}')
        logging.warning(f'[DEBUG] undo() - Ação a ser desfeita: {action[3]}')
        logging.warning(f'[DEBUG] undo() - Dados serializados: {list(action[0].keys())}')
        
        # Recriar blocos a partir dos dados serializados
        serialized_blocks = action[0]
        self.diagram.blocks = {}
        for block_id, block_data in serialized_blocks.items():
            # Criar novo BlockModel a partir dos dados serializados
            from mosaicode.model.blockmodel import BlockModel
            new_block = BlockModel()
            for key, value in block_data.items():
                if hasattr(new_block, key):
                    setattr(new_block, key, value)
            self.diagram.blocks[block_id] = new_block
            logging.warning(f'[DEBUG] undo() - Bloco recriado: {new_block.type} (ID: {new_block.id})')
        
        # Recriar conectores como objetos ConnectionModel
        serialized_connectors = action[1]
        self.diagram.connectors = []
        for conn_data in serialized_connectors:
            try:
                # Encontrar os blocos de entrada e saída
                output_block = None
                input_block = None
                if conn_data.get('output') and 'id' in conn_data['output']:
                    output_id = conn_data['output']['id']
                    if output_id in self.diagram.blocks:
                        output_block = self.diagram.blocks[output_id]
                
                if conn_data.get('input') and 'id' in conn_data['input']:
                    input_id = conn_data['input']['id']
                    if input_id in self.diagram.blocks:
                        input_block = self.diagram.blocks[input_id]
                
                # Criar nova conexão apenas se ambos os blocos existirem
                if output_block and input_block:
                    from mosaicode.model.connectionmodel import ConnectionModel
                    new_connection = ConnectionModel(
                        diagram=self.diagram,
                        output=output_block,
                        output_port=conn_data.get('output_port'),
                        input=input_block,
                        input_port=conn_data.get('input_port')
                    )
                    self.diagram.connectors.append(new_connection)
                    logging.warning(f'[DEBUG] undo() - Conexão recriada: {output_block.id} -> {input_block.id}')
            except Exception as e:
                logging.warning(f'[DEBUG] undo() - Erro ao recriar conexão: {e}')
                continue
        
        # Recriar comentários
        serialized_comments = action[2]
        self.diagram.comments = []
        for comment_data in serialized_comments:
            try:
                from mosaicode.model.commentmodel import CommentModel
                new_comment = CommentModel()
                new_comment.id = comment_data.get('id', -1)
                new_comment.x = comment_data.get('x', 0)
                new_comment.y = comment_data.get('y', 0)
                # Definir propriedades se houver texto
                if 'text' in comment_data:
                    new_comment.properties = [{
                        'name': 'text',
                        'value': comment_data['text'],
                        'type': 'comment'
                    }]
                self.diagram.comments.append(new_comment)
                logging.warning(f'[DEBUG] undo() - Comentário recriado: {new_comment.id}')
            except Exception as e:
                logging.warning(f'[DEBUG] undo() - Erro ao recriar comentário: {e}')
                continue
        
        msg: str = action[3]
        logging.warning(f'[DEBUG] undo() - Blocos após recriação: {list(self.diagram.blocks.keys())}')
        self.diagram.redraw()
        logging.warning(f'[DEBUG] undo_stack: {len(self.diagram.undo_stack)}, redo_stack: {len(self.diagram.redo_stack)}')
        logging.warning(f'[DEBUG] Blocos após undo: {list(self.diagram.blocks.keys())}')

    # ---------------------------------------------------------------------
    def redo(self) -> None:
        logging.warning('[DEBUG] DiagramControl.redo chamado')
        if len(self.diagram.redo_stack) < 1:
            logging.warning('[DEBUG] redo_stack vazio')
            return
        self.diagram.set_modified(True)
        
        # Salvar o estado atual no undo_stack antes de restaurar
        current_state = self._serialize_current_state("Current State")
        self.diagram.undo_stack.append(current_state)
        
        action: Tuple[Dict[int, Any], List[Any], List[Any], str] = self.diagram.redo_stack.pop()
        
        logging.warning(f'[DEBUG] redo() - Blocos antes: {list(self.diagram.blocks.keys())}')
        logging.warning(f'[DEBUG] redo() - Ação a ser refeita: {action[3]}')
        logging.warning(f'[DEBUG] redo() - Dados serializados: {list(action[0].keys())}')
        
        # Recriar blocos a partir dos dados serializados
        serialized_blocks = action[0]
        self.diagram.blocks = {}
        for block_id, block_data in serialized_blocks.items():
            # Criar novo BlockModel a partir dos dados serializados
            from mosaicode.model.blockmodel import BlockModel
            new_block = BlockModel()
            for key, value in block_data.items():
                if hasattr(new_block, key):
                    setattr(new_block, key, value)
            self.diagram.blocks[block_id] = new_block
            logging.warning(f'[DEBUG] redo() - Bloco recriado: {new_block.type} (ID: {new_block.id})')
        
        # Recriar conectores como objetos ConnectionModel
        serialized_connectors = action[1]
        self.diagram.connectors = []
        for conn_data in serialized_connectors:
            try:
                # Encontrar os blocos de entrada e saída
                output_block = None
                input_block = None
                if conn_data.get('output') and 'id' in conn_data['output']:
                    output_id = conn_data['output']['id']
                    if output_id in self.diagram.blocks:
                        output_block = self.diagram.blocks[output_id]
                
                if conn_data.get('input') and 'id' in conn_data['input']:
                    input_id = conn_data['input']['id']
                    if input_id in self.diagram.blocks:
                        input_block = self.diagram.blocks[input_id]
                
                # Criar nova conexão apenas se ambos os blocos existirem
                if output_block and input_block:
                    from mosaicode.model.connectionmodel import ConnectionModel
                    new_connection = ConnectionModel(
                        diagram=self.diagram,
                        output=output_block,
                        output_port=conn_data.get('output_port'),
                        input=input_block,
                        input_port=conn_data.get('input_port')
                    )
                    self.diagram.connectors.append(new_connection)
                    logging.warning(f'[DEBUG] redo() - Conexão recriada: {output_block.id} -> {input_block.id}')
            except Exception as e:
                logging.warning(f'[DEBUG] redo() - Erro ao recriar conexão: {e}')
                continue
        
        # Recriar comentários
        serialized_comments = action[2]
        self.diagram.comments = []
        for comment_data in serialized_comments:
            try:
                from mosaicode.model.commentmodel import CommentModel
                new_comment = CommentModel()
                new_comment.id = comment_data.get('id', -1)
                new_comment.x = comment_data.get('x', 0)
                new_comment.y = comment_data.get('y', 0)
                # Definir propriedades se houver texto
                if 'text' in comment_data:
                    new_comment.properties = [{
                        'name': 'text',
                        'value': comment_data['text'],
                        'type': 'comment'
                    }]
                self.diagram.comments.append(new_comment)
                logging.warning(f'[DEBUG] redo() - Comentário recriado: {new_comment.id}')
            except Exception as e:
                logging.warning(f'[DEBUG] redo() - Erro ao recriar comentário: {e}')
                continue
        
        msg: str = action[3]
        logging.warning(f'[DEBUG] redo() - Blocos após recriação: {list(self.diagram.blocks.keys())}')
        self.diagram.redraw()
        logging.warning(f'[DEBUG] undo_stack: {len(self.diagram.undo_stack)}, redo_stack: {len(self.diagram.redo_stack)}')
        logging.warning(f'[DEBUG] Blocos após redo: {list(self.diagram.blocks.keys())}')
        
    # ---------------------------------------------------------------------
    def _serialize_current_state(self, msg: str) -> Tuple[Dict[int, Any], List[Any], List[Any], str]:
        """
        Serialize the current state of the diagram.
        
        Args:
            msg: Message describing the state
            
        Returns:
            Serialized state tuple
        """
        # Serializar os blocos para evitar problemas com GObject
        serialized_blocks = {}
        for block_id, block in self.diagram.blocks.items():
            # Criar uma cópia serializada do bloco
            serialized_block = {
                'id': block.id,
                'type': block.type,
                'language': block.language,
                'x': block.x,
                'y': block.y,
                'label': block.label,
                'color': block.color,
                'group': block.group,
                'help': block.help,
                'version': block.version,
                'extension': block.extension,
                'file': block.file,
                'is_collapsed': block.is_collapsed,
                'ports': block.ports.copy() if hasattr(block, 'ports') else [],
                'properties': block.properties.copy() if hasattr(block, 'properties') else [],
                'codes': block.codes.copy() if hasattr(block, 'codes') else {},
                'gen_codes': block.gen_codes.copy() if hasattr(block, 'gen_codes') else {},
                'weight': block.weight,
                'connections': block.connections.copy() if hasattr(block, 'connections') else [],
                'maxIO': block.maxIO
            }
            serialized_blocks[block_id] = serialized_block
        
        # Serializar conectores e comentários
        serialized_connectors = []
        for conn in self.diagram.connectors:
            serialized_conn = {
                'output': {'id': conn.output.id} if hasattr(conn, 'output') and conn.output else None,
                'input': {'id': conn.input.id} if hasattr(conn, 'input') and conn.input else None,
                'output_port': conn.output_port,
                'input_port': conn.input_port
            }
            serialized_connectors.append(serialized_conn)
        
        serialized_comments = []
        for comment in self.diagram.comments:
            # Get text from properties
            text = ""
            if hasattr(comment, 'get_properties') and comment.get_properties():
                for prop in comment.get_properties():
                    if prop.get('name') == 'text':
                        text = prop.get('value', '')
                        break
            
            serialized_comment = {
                'id': comment.id,
                'x': comment.x,
                'y': comment.y,
                'text': text,
                'color': getattr(comment, 'color', 'black')
            }
            serialized_comments.append(serialized_comment)
        
        return (serialized_blocks, serialized_connectors, serialized_comments, msg)

    # ----------------------------------------------------------------------
    def load(self, file_name: Optional[str] = None) -> bool:
        """
        This method load a file.

        Args:
            file_name: Path to the file to load
            
        Returns:
            True if loading was successful, False otherwise
        """
        if file_name is not None:
            self.diagram.file_name = file_name
        else:
            if self.diagram.file_name is None:
                System.log("Cannot Load without filename")
                return False
        if not Path(self.diagram.file_name).exists():
            System.log("File '" + self.diagram.file_name +
                       "' does not exist!")
            return False

        result: bool = DiagramPersistence.load(self.diagram)
        self.diagram.redo_stack = []
        self.diagram.undo_stack = []

        return result

    # ----------------------------------------------------------------------
    def save(self) -> Tuple[bool, str]:
        """
        This method save a file.

        Returns:
            Tuple of (success, message)
        """
        return DiagramPersistence.save(self.diagram)

    # ----------------------------------------------------------------------
    def get_min_max(self) -> Tuple[int, int, int, int]:
        """
        This method get min and max coordinates with margins to avoid cutting blocks.
        
        Returns:
            Tuple of (min_x, min_y, width, height)
        """
        min_x: int = self.diagram.main_window.get_size()[0]
        min_y: int = self.diagram.main_window.get_size()[1]

        max_x: int = 0
        max_y: int = 0

        # If no blocks, return default area
        if not self.diagram.blocks:
            return 0, 0, 800, 600

        for block_id in self.diagram.blocks:
            block: Any = self.diagram.blocks[block_id]
            x: int
            y: int
            x, y = block.get_position()
            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y
            if x + block.width > max_x:
                max_x = x + block.width
            if y + block.height > max_y:
                max_y = y + block.height

        # Add margins to avoid cutting blocks
        margin = 50
        width = max_x - min_x + (2 * margin)
        height = max_y - min_y + (2 * margin)
        
        # Ensure minimum size
        if width < 400:
            width = 400
        if height < 300:
            height = 300

        return min_x - margin, min_y - margin, width, height

    # ----------------------------------------------------------------------
    def export_png(self, file_name: str = "diagrama.png") -> Tuple[bool, str]:
        """
        This method export a png.

        Args:
            file_name: Path to save the PNG file
            
        Returns:
            Tuple of (success, message)
        """
        if file_name is None:
            file_name = "diagrama.png"

        x: int
        y: int
        width: int
        height: int
        x, y, width, height = self.get_min_max()

        if x < 0 or y < 0:
            self.diagram.reload()
            x, y, width, height = self.get_min_max()

        if self.diagram.get_window() is None:
            return False, "Diagram has no window"
        pixbuf: Optional[Gdk.Pixbuf] = Gdk.pixbuf_get_from_window(
                        self.diagram.get_window(),
                        x,
                        y,
                        width,
                        height)

        if pixbuf is None:
            return False, "No image to export"

        test: bool
        tmp_buffer: bytes
        test, tmp_buffer = pixbuf.save_to_bufferv("png",  [], [])

        try:
            save_file = open(file_name, "wb")
            save_file.write(tmp_buffer)
            save_file.close()
            return True, "Image exported successfully"
        except Exception as error:
            return False, f"Error saving file: {error}"

# ----------------------------------------------------------------------

# -*- coding: utf-8 -*-
"""
This module contains the Diagram class.
"""
import gi
import logging
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GooCanvas', '2.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GooCanvas
from typing import Any, Optional, List, Dict, Tuple
from mosaicode.GUI.block import Block
from mosaicode.GUI.connector import Connector
from mosaicode.GUI.comment import Comment
from mosaicode.system import System as System
from mosaicode.model.diagrammodel import DiagramModel
from mosaicode.model.blockmodel import BlockModel
from mosaicode.control.diagramcontrol import DiagramControl
import gettext
_ = gettext.gettext


class Diagram(GooCanvas.Canvas, DiagramModel):
    """
    This class contains the methods related to Diagram class.
    """

    # ----------------------------------------------------------------------

    def __init__(self, main_window: Any) -> None:
        GooCanvas.Canvas.__init__(self)
        DiagramModel.__init__(self)
        self.set_property("expand", True)
        self.set_property("has-tooltip", True)  # Allow tooltip on elements
        self.set_property("background-color", "White")
        self.set_property("clear-background", True)
        Gtk.Widget.grab_focus(self)

        self.last_clicked_point: Tuple[Optional[float], Optional[float]] = (None, None)
        self.main_window: Any = main_window

        self.curr_connector: Optional[Connector] = None

        self.connect("motion-notify-event", self.__on_motion_notify)
        self.connect_after("button_press_event", self.__on_button_press)
        self.connect_after("button_release_event", self.__on_button_release)
        self.connect_after("key-press-event", self.__on_key_press)

        self.connect("drag_data_received", self.__drag_data_received)
        self.drag_dest_set(
            Gtk.DestDefaults.MOTION |
            Gtk.DestDefaults.HIGHLIGHT |
            Gtk.DestDefaults.DROP,
            [Gtk.TargetEntry.new('text/plain', Gtk.TargetFlags.SAME_APP, 1)],
            Gdk.DragAction.DEFAULT | Gdk.DragAction.COPY)

        self.show_grid: bool = False
        self.select_rect: Optional[Any] = None
        self.__draw_grid()

        # Used for cycle detection
        self.show()

    # ----------------------------------------------------------------------
    def __on_motion_notify(self, canvas_item, event):
        scale = self.get_scale()
        # Select elements
        if self.select_rect is not None:
            self.__update_select(event.x / scale, event.y / scale)
            items = self.get_items_in_area(
                self.select_rect.bounds, True, False, True)
            for item in items:
                    item.is_selected = True
            self.update_flows()
            return True  # Abort other events

        if event.state & Gdk.ModifierType.BUTTON1_MASK:
            for connector in self.connectors:
                connector.update_flow()

        if self.curr_connector is None:
            return False
        point = (event.x / scale, event.y / scale)
        self.curr_connector.update_flow(point)
        return False

    # ----------------------------------------------------------------------
    def __on_key_press(self, widget, event=None):
        grid = System.get_preferences().grid
        modifier_mask = Gtk.accelerator_get_default_mod_mask()
        event.state = event.state & modifier_mask

        if event.state == Gdk.ModifierType.CONTROL_MASK:
            if event.keyval == Gdk.KEY_Up:
                self.move_selected(0, -grid*5)
                return True
            if event.keyval == Gdk.KEY_Down:
                self.move_selected(0, grid*5)
                return True
            if event.keyval == Gdk.KEY_Left:
                self.move_selected(-grid*5, 0)
                return True
            if event.keyval == Gdk.KEY_Right:
                self.move_selected(grid*5, 0)
                return True

        if event.keyval == Gdk.KEY_Delete and self.focus:
            self.delete()
            return True

        if event.keyval == Gdk.KEY_Up:
            self.move_selected(0, -grid)
            return True
        if event.keyval == Gdk.KEY_Down:
            self.move_selected(0, grid)
            return True
        if event.keyval == Gdk.KEY_Left:
            self.move_selected(-grid, 0)
            return True
        if event.keyval == Gdk.KEY_Right:
            self.move_selected(grid, 0)
            return True

    # ----------------------------------------------------------------------
    def __on_button_release(self, widget, event=None):
        self.__end_select()

    # ----------------------------------------------------------------------
    def __on_button_press(self, widget, event=None):
        Gtk.Widget.grab_focus(self)
        if event.button == 1:
            self.main_window.property_box.set_diagram(self)
            self.last_clicked_point = (event.x, event.y)
            self.deselect_all()
            self.__abort_connection()
            self.update_flows()
            self.__start_select()
            return False
        if event.button == 3:
            self.main_window.diagram_menu.show(self, event)
            return False
        return False

    # ----------------------------------------------------------------------
    def __start_select(self):
        if self.select_rect is None:
            self.select_rect = GooCanvas.CanvasRect(
                parent=self.get_root_item(),
                x=self.last_clicked_point[0],
                y=self.last_clicked_point[1],
                width=0,
                height=0,
                stroke_color="black",
                fill_color=None,
                line_dash=GooCanvas.CanvasLineDash.newv((4.0, 4.0))
            )

    # ----------------------------------------------------------------------
    def __end_select(self):
        if self.select_rect is not None:
            self.select_rect.remove()
            del self.select_rect
            self.select_rect = None

    # ----------------------------------------------------------------------
    def __update_select(self, x, y):
        scale = self.get_scale()
        xi = 0
        xf = 0
        yi = 0
        yf = 0
        if x > self.last_clicked_point[0] / scale:
            xi = self.last_clicked_point[0] / scale
            xf = x
        else:
            xi = x
            xf = self.last_clicked_point[0] / scale
        if y > self.last_clicked_point[1] / scale:
            yi = self.last_clicked_point[1] / scale
            yf = y
        else:
            yi = y
            yf = self.last_clicked_point[1] / scale
        self.select_rect.set_property("x", xi)
        self.select_rect.set_property("width", xf - xi)
        self.select_rect.set_property("y", yi)
        self.select_rect.set_property("height", yf - yi)

    # ----------------------------------------------------------------------
    def __drag_data_received(self, widget, context, x, y, selection,
                             targetType, time):
        block = self.main_window.main_control.get_selected_block()
        if block is not None:
            block.x = x
            block.y = y
            self.main_window.main_control.add_block(block)
        return

    # ----------------------------------------------------------------------
    def __valid_connector(self, newCon: Connector) -> bool:
        """
        Parameters:

        Returns
             * **Types** (:class:`boolean<boolean>`)
        """
        for oldCon in self.connectors:
            if oldCon.input == newCon.input \
                    and oldCon.input_port == newCon.input_port\
                    and not newCon.input_port.multiple:
                System.log(_("Connector Already exists"))
                return False
        if (newCon.input == newCon.output) or self.__cycle_detection(newCon):
            System.log(_("Recursive connection is not allowed"))
            return False
        if newCon.input_port.type != newCon.output_port.type:
            System.log(_("Connection Types mismatch"))
            return False
        return True

    # ----------------------------------------------------------------------
    def __cycle_detection(self, newCon: Connector) -> bool:
        marks = []
        marks.append(newCon.input.id)
        i = 0
        while i < len(marks):
            for connection in self.connectors:
                if connection.output.id != marks[i]:
                    continue
                if connection.input == newCon.output:
                    return True
                if connection.input.id not in marks:
                    marks.append(connection.input.id)
            i += 1
        return False

    # ----------------------------------------------------------------------
    def __abort_connection(self):
        if self.curr_connector is None:
            return
        connector_number = self.get_root_item().find_child(self.curr_connector)
        self.get_root_item().remove_child(connector_number)
        del self.curr_connector
        self.curr_connector = None

    # ----------------------------------------------------------------------
    def start_connection(self, block, port):
        """
        This method start a connection.

            Parameters:
                * **block**
                * **output**

        """
        self.__abort_connection()  # abort any possibly running connections
        self.curr_connector = Connector(self, block, port)
        self.get_root_item().add_child(self.curr_connector, -1)
        self.update_flows()

    # ----------------------------------------------------------------------
    def end_connection(self, block, port):
        """
        This method end a connection.

            Parameters:
                * **block**
                * **port**
            Returns:
                * **Types** (:class:`boolean<boolean>`)
        """
        if self.curr_connector is None:
            return False
        self.curr_connector.input = block
        self.curr_connector.input_port = port
        if not self.__valid_connector(self.curr_connector):
            self.__abort_connection()
            return False

        self.connectors.append(self.curr_connector)
        self.curr_connector = None
        self.update_flows()
        return True

    # ----------------------------------------------------------------------
    def __draw_grid(self):
        if self.show_grid:
            width = self.main_window.get_size()[0]
            height = self.main_window.get_size()[1]

            i = 0
            while i < height:
                GooCanvas.CanvasPath(
                        parent=self.get_root_item(),
                        stroke_color="#F9F9F9",
                        data="M 0 " + str(i) + " L "+ str(width) +" "+ str(i) + "",
                        line_width=0.8
                        )
                i = i + System.get_preferences().grid
            i = 0
            while i < width:
                GooCanvas.CanvasPath(
                        parent=self.get_root_item(),
                        stroke_color="#F9F9F9",
                        data="M " + str(i) + " 0 L "+ str(i) + " "+ str(height) +"",
                        line_width=0.8
                        )
                i = i + System.get_preferences().grid

    # ----------------------------------------------------------------------
    def update_flows(self):
        """
        This method update flows.
        """
        self.update()
        for block_id in self.blocks:
            self.blocks[block_id].update_flow()
        for conn in self.connectors:
            conn.update_flow()
        for comment in self.comments:
            if hasattr(comment, 'update_flow'):
                comment.update_flow()

    # ----------------------------------------------------------------------
    def change_zoom(self, value):
        """
        This method change zoom.

            Parameters:
               * **value** (:class:`float<float>`)
        """
        zoom = self.zoom
        if value == System.ZOOM_ORIGINAL:
            zoom = System.ZOOM_ORIGINAL
        elif value == System.ZOOM_IN:
            zoom = zoom + 0.1
        elif value == System.ZOOM_OUT:
            zoom = zoom - 0.1
        self.zoom = zoom
        self.set_scale(self.zoom)
        self.update_flows()
        self.set_modified(True)

    # ----------------------------------------------------------------------
    def zoom_in(self) -> None:
        """
        Zoom in on the diagram.
        """
        self.change_zoom(System.ZOOM_IN)

    # ----------------------------------------------------------------------
    def zoom_out(self) -> None:
        """
        Zoom out on the diagram.
        """
        self.change_zoom(System.ZOOM_OUT)

    # ----------------------------------------------------------------------
    def zoom_normal(self) -> None:
        """
        Reset zoom to normal on the diagram.
        """
        self.change_zoom(System.ZOOM_ORIGINAL)

    # ----------------------------------------------------------------------
    def align_top(self) -> None:
        """
        Align selected blocks to top.
        """
        logging.debug(r"Diagram.align_top() chamado")
        diagram_control = DiagramControl(self)
        diagram_control.align("TOP")
        self.update_flows()
        self.redraw()
        logging.debug(r"Diagram.align_top() - atualização visual concluída")

    # ----------------------------------------------------------------------
    def align_bottom(self) -> None:
        """
        Align selected blocks to bottom.
        """
        logging.debug(r"Diagram.align_bottom() chamado")
        diagram_control = DiagramControl(self)
        diagram_control.align("BOTTOM")
        self.update_flows()
        self.redraw()
        logging.debug(r"Diagram.align_bottom() - atualização visual concluída")

    # ----------------------------------------------------------------------
    def align_left(self) -> None:
        """
        Align selected blocks to left.
        """
        logging.debug(r"Diagram.align_left() chamado")
        diagram_control = DiagramControl(self)
        diagram_control.align("LEFT")
        self.update_flows()
        self.redraw()
        logging.debug(r"Diagram.align_left() - atualização visual concluída")

    # ----------------------------------------------------------------------
    def align_right(self) -> None:
        """
        Align selected blocks to right.
        """
        logging.debug(r"Diagram.align_right() chamado")
        diagram_control = DiagramControl(self)
        diagram_control.align("RIGHT")
        self.update_flows()
        self.redraw()
        logging.debug(r"Diagram.align_right() - atualização visual concluída")

    # ----------------------------------------------------------------------
    def collapse_all(self) -> None:
        """
        Collapse all blocks in the diagram.
        """
        diagram_control = DiagramControl(self)
        diagram_control.collapse_all(True)

    # ----------------------------------------------------------------------
    def uncollapse_all(self) -> None:
        """
        Uncollapse all blocks in the diagram.
        """
        diagram_control = DiagramControl(self)
        diagram_control.collapse_all(False)

    # ----------------------------------------------------------------------
    def undo(self) -> None:
        """
        Undo last action.
        """
        logging.debug(r"Diagram.undo() chamado")
        diagram_control = DiagramControl(self)
        diagram_control.undo()
        self.update_flows()
        self.redraw()
        logging.debug(r"Diagram.undo() - atualização visual concluída")

    # ----------------------------------------------------------------------
    def redo(self) -> None:
        """
        Redo last undone action.
        """
        logging.debug(r"Diagram.redo() chamado")
        diagram_control = DiagramControl(self)
        diagram_control.redo()
        self.update_flows()
        self.redraw()
        logging.debug(r"Diagram.redo() - atualização visual concluída")

    # ----------------------------------------------------------------------
    def delete(self) -> None:
        """
        Delete selected elements.
        """
        logging.debug(r"Diagram.delete() chamado")
        diagram_control = DiagramControl(self)
        diagram_control.delete()
        self.update_flows()
        self.redraw()
        logging.debug(r"Diagram.delete() - atualização visual concluída")

    # ----------------------------------------------------------------------
    def add_comment(self, comment=None) -> None:
        """
        Add a comment to the diagram.
        """
        diagram_control = DiagramControl(self)
        diagram_control.add_comment(comment)

    # ----------------------------------------------------------------------
    def copy(self) -> None:
        """
        Copy selected elements.
        """
        logging.debug(r"Diagram.copy() chamado")
        diagram_control = DiagramControl(self)
        diagram_control.copy()
        self.update_flows()
        self.redraw()
        logging.debug(r"Diagram.copy() - atualização visual concluída")

    # ----------------------------------------------------------------------
    def paste(self) -> None:
        """
        Paste elements from clipboard.
        """
        logging.debug(r"Diagram.paste() chamado")
        diagram_control = DiagramControl(self)
        diagram_control.paste()
        self.update_flows()
        self.redraw()
        logging.debug(r"Diagram.paste() - atualização visual concluída")

    # ----------------------------------------------------------------------
    def cut(self) -> None:
        """
        Cut selected elements.
        """
        logging.debug(r"Diagram.cut() chamado")
        diagram_control = DiagramControl(self)
        diagram_control.cut()
        self.update_flows()
        self.redraw()
        logging.debug(r"Diagram.cut() - atualização visual concluída")

    # ----------------------------------------------------------------------
    def show_comment_property(self, comment):
        """
        This method show comment property.

            Parameters:
                * **block**(:class: `Block<mosaicode.GUI.block>`)
        """
        self.main_window.property_box.set_comment(comment)

    # ----------------------------------------------------------------------
    def show_block_property(self, block):
        logging.debug(r"Diagram.show_block_property chamado para: {getattr(block, 'label', None)}")
        logging.debug(r"Propriedades do bloco: {len(getattr(block, 'properties', []))}")
        self.main_window.property_box.set_block(block)

    # ----------------------------------------------------------------------
    def resize(self, data):
        """
        This method resize diagram.

            Parameters:
               * **data**
        """
        value = self.main_window.get_size()[0]
        self.set_property("x2", value)

    # ----------------------------------------------------------------------
    def deselect_all(self):
        for key in self.blocks:
            self.blocks[key].is_selected = False
        for conn in self.connectors:
            conn.is_selected = False
        for comment in self.comments:
            if hasattr(comment, 'is_selected'):
                comment.is_selected = False

    # ----------------------------------------------------------------------
    def select_all(self):
        """
        This method select all blocks in diagram.
        """
        logging.debug(r"Diagram.select_all() chamado")
        for key in self.blocks:
            self.blocks[key].is_selected = True
        for conn in self.connectors:
            conn.is_selected = True
        for comment in self.comments:
            if hasattr(comment, 'is_selected'):
                comment.is_selected = True
        self.update_flows()
        self.redraw()
        Gtk.Widget.grab_focus(self)
        logging.debug(r"Diagram.select_all() - {len(self.blocks)} blocos selecionados")

    # ----------------------------------------------------------------------
    def move_selected(self, x, y):
        """
        This method move selected blocks.

            Parameters:
                * **(x,y)** (:class:`float<float>`)

        """
        for key in self.blocks:
            if not self.blocks[key].is_selected:
                continue
            pos_x, pos_y = self.blocks[key].get_position()
            x, y = self.check_limit(x, y, pos_x, pos_y)
            self.blocks[key].move(x, y)

        for comment in self.comments:
            if not hasattr(comment, 'is_selected') or not comment.is_selected:
                continue
            if hasattr(comment, 'get_position'):
                pos_x, pos_y = comment.get_position()
                x, y = self.check_limit(x, y, pos_x, pos_y)
                comment.move(x, y)
        self.update_flows()

    # ----------------------------------------------------------------------
    def collapse(self, state):
        for key in self.blocks:
            if not self.blocks[key].is_selected:
                continue
            self.blocks[key].is_collapsed = state
        self.update_flows()

    # ---------------------------------------------------------------------
    def check_limit(self, x, y, block_pos_x, block_pos_y):
        min_x = 0
        min_y = 0

        max_x, max_y = self.main_window.get_size()

        new_x = x + block_pos_x
        new_y = y + block_pos_y

        if new_x < min_x:
            x = min_x - block_pos_x
        elif new_x > max_x:
            x = max_x - block_pos_x

        if new_y < min_y:
            y = min_y - block_pos_y
        elif new_y > max_y:
            y = max_y - block_pos_y

        return x, y


    # ---------------------------------------------------------------------
    def set_modified(self, state):
        """
        This method set a modification.

            Parameters:
                * **state**
        """
        self.modified = state
        if hasattr(self.main_window, 'work_area') and self.main_window.work_area is not None:
            self.main_window.work_area.rename_diagram(self)

    # ---------------------------------------------------------------------
    def redraw(self):
        """
        This method redraw the diagram.
        """
        # First, remove all items from the diagram
        while self.get_root_item().get_n_children() != 0:
            self.get_root_item().remove_child(0)
        self.__draw_grid()

        # Check diagram content
        # Create Block widgets
        for key in self.blocks:
            block = self.blocks[key]
            if not isinstance(block, Block):
                block = Block(self, self.blocks[key])
                self.blocks[key] = block

        # Create Connection Widgets
        i = 0
        to_remove = []

        for connector in self.connectors:

            # If it is not an instance of a connector, it is a connection model
            # Probably it it the first time we draw this diagram            
            if not isinstance(connector, Connector):
                outb = self.blocks[connector.output.id]
                conn = Connector(self, outb, connector.output_port)
                conn.input = self.blocks[connector.input.id]
                conn.input_port = connector.input_port
                connector = conn
                self.connectors[i] = conn

            if connector.output:
                if  connector.output.id not in self.blocks or \
                        connector.input.id not in self.blocks:
                    to_remove.append(connector)
            i = i + 1
        for conn in to_remove:
            self.connectors.remove(conn)

        # Create Comment Widgets
        i = 0
        for comment in self.comments:
            if not isinstance(comment, Comment):
                # Se é um dicionário (dados serializados), criar CommentModel primeiro
                if isinstance(comment, dict):
                    from mosaicode.model.commentmodel import CommentModel
                    comment_model = CommentModel()
                    comment_model.id = comment.get('id', -1)
                    comment_model.x = comment.get('x', 0)
                    comment_model.y = comment.get('y', 0)
                    # Restaurar propriedades
                    if 'text' in comment:
                        comment_model.properties[0]["value"] = comment['text']
                    comm = Comment(self, comment_model)
                else:
                    comm = Comment(self, comment)
                # Acessar x e y de forma segura
                x = comment.get('x', 0) if isinstance(comment, dict) else comment.x
                y = comment.get('y', 0) if isinstance(comment, dict) else comment.y
                comm.move(x, y)
                comm.update_flow()
                self.comments[i] = comm
            i = i + 1

        # Redraw Blocks
        for key in self.blocks:
            block = self.blocks[key]
            if not isinstance(block, Block):
                block = Block(self, self.blocks[key])
                self.blocks[key] = block
            self.get_root_item().add_child(block, -1)
            block.adjust_position()
        i = 0

        # Redraw Connections
        for connector in self.connectors:
            if not isinstance(connector, Connector) and connector.output:
                outb = self.blocks[connector.output.id]
                conn = Connector(self, outb, connector.output_port)
                conn.input = self.blocks[connector.input.id]
                conn.input_port = connector.input_port
                connector = conn
                self.connectors[i] = conn
            if isinstance(connector, GooCanvas.CanvasItem):
                self.get_root_item().add_child(connector, -1)
            i = i + 1

        # Redraw Comments
        for comment in self.comments:
            self.get_root_item().add_child(comment, -1)
            comment.adjust_position()

        self.update_flows()

    # ----------------------------------------------------------------------
    def show_block_menu(self, block, event):
        self.main_window.block_menu.show(block, event)

    # ----------------------------------------------------------------------
    def toggle_grid(self, event: Any = None) -> None:
        """
        Alterna a visibilidade da grade.
        Args:
            event: O evento que disparou a alternância (opcional)
        """
        self.show_grid = not self.show_grid
        self.redraw()

# ----------------------------------------------------------------------

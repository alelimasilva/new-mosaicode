# -*- coding: utf-8 -*-
# noqa: E402
"""
This module contains the Block class.
"""
import os
import gi
import logging
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GooCanvas', '2.0')
gi.require_version('PangoCairo', '1.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GooCanvas
from gi.repository import GdkPixbuf
from gi.repository import Pango
from typing import Any, Optional, Dict, List, Tuple
from mosaicode.system import System
from mosaicode.model.blockmodel import BlockModel
from mosaicode.model.port import Port


class Block(GooCanvas.CanvasGroup, BlockModel):
    """
    This class contains methods related the Block class
    """

    # ----------------------------------------------------------------------

    def __init__(self, diagram: Any, block: Optional[BlockModel] = None) -> None:
        """
        This method is the constuctor.
        """
        GooCanvas.CanvasGroup.__init__(self)
        if block is not None:
            # Copia todos os atributos do BlockModel fornecido
            for field_name in block.__dataclass_fields__:
                setattr(self, field_name, getattr(block, field_name))
        else:
            BlockModel.__init__(self)
        self.diagram = diagram
        self.selected = False

        self.remember_x: int = 0
        self.remember_y: int = 0

        self.widgets: Dict[str, Any] = {}
        self.focus: bool = False
        self.has_flow: bool = False
        self.is_selected: bool = False
        self.is_collapsed: bool = False

        self.width: int = 112

        self.connect("button-press-event", self.__on_button_press)
        self.connect("motion-notify-event", self.__on_motion_notify)
        self.connect("enter-notify-event", self.__on_enter_notify)
        self.connect("leave-notify-event", self.__on_leave_notify)
        self.move(int(float(self.x)), int(float(self.y)))

        self.height: int = self.__calculate_height()

        self.__draw_rect()
        self.__draw_label()
        self.__draw_ports()
        self.__draw_icon()
        self.update_flow()

    # ----------------------------------------------------------------------
    def __on_button_press(self, canvas_item: Any, target_item: Any, event: Gdk.Event) -> bool:
        """
        This method monitors when the button is pressed.

            Parameters:
                canvas_item
            Returns:
                * **Types** (:class:`boolean<boolean>`)
                Indicates the button is pressed.
            """
        logging.debug(r"Block.__on_button_press chamado para: {getattr(self, 'label', None)}")
        # with Shift
        if event.state == Gdk.ModifierType.SHIFT_MASK \
                | Gdk.ModifierType.MOD2_MASK:
            if self.is_selected:
                self.is_selected = False
            else:
                self.is_selected = True

        else:
            if not self.is_selected:
                self.diagram.deselect_all()
                self.is_selected = True

        self.diagram.show_block_property(self)

        if event.button == 1:
            self.remember_x = event.x
            self.remember_y = event.y

        self.diagram.update_flows()

        if event.button == 3:
            return False

        return True

    # ----------------------------------------------------------------------
    def __on_motion_notify(self, canvas_item: Any, target_item: Any, event: Optional[Gdk.Event] = None) -> bool:
        """
        This method monitors the motion.

            Parameters:
                canvas_item
                target_item

            Returns:
                * **Types** (:class:`boolean<boolean>`)

        """
        if not event.state & Gdk.ModifierType.BUTTON1_MASK:
            return False
        if self.diagram.curr_connector is not None:
            return False
        # Get the new position and move by the difference
        new_x = event.x - self.remember_x
        new_y = event.y - self.remember_y
        self.diagram.move_selected(new_x, new_y)
        return False

    # ----------------------------------------------------------------------
    def __on_enter_notify(self, canvas_item: Any, target_item: Any, event: Optional[Gdk.Event] = None) -> bool:
        """
        This method monitors the motion.

            Parameters:
                canvas_item
            Returns:
                * **TYpes** (:class:`boolean<boolean>`)
        """
        self.focus = True
        self.__update_state()
        return False

    # ----------------------------------------------------------------------
    def __on_leave_notify(self, canvas_item: Any, target_item: Any, event: Optional[Gdk.Event] = None) -> bool:
        """
        This method monitors the motion.

            Parameters:
                canvas_item
                target_item

            Returns:
                * **Types** (:class:`boolean<boolean>`)

        """
        self.focus = False
        self.__update_state()
        return False

    # ----------------------------------------------------------------------
    def get_color_as_guint(self) -> int:
        """
        Converte a cor para o formato guint esperado pelo GooCanvas.
        
        Returns:
            int: Valor guint da cor
        """
        color_str = self.get_color_as_rgba()
        
        # Se a cor começa com #, é um valor hexadecimal
        if color_str.startswith("#"):
            # Remove o # e converte para inteiro
            hex_color = color_str[1:]
            if len(hex_color) == 6:  # RGB
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                # Converte para formato RGBA (A=255 para opaco)
                return (r << 24) | (g << 16) | (b << 8) | 255
            elif len(hex_color) == 8:  # RGBA
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                a = int(hex_color[6:8], 16)
                return (r << 24) | (g << 16) | (b << 8) | a
        
        # Se a cor está no formato rgba(r,g,b,a)
        elif color_str.startswith("rgba("):
            # Extrai os valores R,G,B,A
            values = color_str[5:-1].split(",")
            if len(values) == 4:
                r = int(float(values[0].strip()))
                g = int(float(values[1].strip()))
                b = int(float(values[2].strip()))
                a = int(float(values[3].strip()))
                return (r << 24) | (g << 16) | (b << 8) | a
        
        # Cor padrão se não conseguir converter
        return 0xFF000000  # Preto opaco

    # ----------------------------------------------------------------------
    def __draw_rect(self) -> None:
        logging.debug(r"__draw_rect: width={self.width}, height={self.height}, x=0, y=10")
        rect = GooCanvas.CanvasRect(parent=self,
                                    x=0,
                                    y=10,
                                    width=self.width,
                                    height=self.height - 15,
                                    radius_x=10,
                                    radius_y=10,
                                    stroke_color="black",
                                    fill_color_rgba=self.get_color_as_guint(),
                                    tooltip=self.label
                                    )
        self.widgets["Rect"] = rect

    # ----------------------------------------------------------------------
    def __draw_icon(self) -> None:
        """
        This method draw a icon.
        """
        text_label = "<span font_family ='Arial' " + \
            "size = '25000' weight = 'bold' > " + \
            self.label.title()[0] + "</span>"

        icon = GooCanvas.CanvasText(parent=self,
                                    text=text_label,
                                    fill_color='white',
                                    anchor=GooCanvas.CanvasAnchorType.CENTER,
                                    x=(self.width / 2),
                                    y=(self.height / 2),
                                    use_markup=True,
                                    stroke_color='black',
                                    tooltip=self.label
                                    )

        self.widgets["Icon"] = icon

    # ----------------------------------------------------------------------
    def __draw_label(self) -> None:
        """
        This method draw the label.

        """
        text_label = "<span font_family ='Arial' " + \
            "size = '10000' weight = 'normal'> " + \
            self.label + "</span>"

        label = GooCanvas.CanvasText(parent=self,
                                     text=text_label,
                                     fill_color='black',
                                     anchor=GooCanvas.CanvasAnchorType.CENTER,
                                     x=(self.width / 2),
                                     y=0,
                                     use_markup=True,
                                     stroke_color='black'
                                     )
        self.widgets["Label"] = label

    # ----------------------------------------------------------------------
    def __create_ports_label(self, port: Port) -> str:
        # Extrai apenas o nome simples do tipo
        tipo = port.hint if port.hint else port.type
        if tipo and '.' in tipo:
            tipo = tipo.split('.')[-1]
        tipo = f"[{tipo.upper()}]"
        # Define cor: preto para FLOAT, vermelho para outros tipos, a menos que port.color esteja definido
        cor = port.color if port.color and port.color not in ('#000', '#000000', '#FFFFFF', '#FFF', 'white') else None
        if not cor:
            if tipo == '[FLOAT]':
                cor = '#000000'
            else:
                cor = '#FF0000'
        text_name = "<span font_family ='Arial' size = '7000' weight = 'ultralight'>" + \
            f"<span color = '{cor}'>{tipo}</span></span>"
        return text_name

    # ----------------------------------------------------------------------
    def __draw_ports(self) -> None:
        logging.debug(r"__draw_ports chamado para bloco: {getattr(self, 'label', None)}")
        logging.debug(r"Número de portas: {len(self.ports)}")
        logging.debug(r"self.width no __draw_ports: {self.width}")
        for i, port in enumerate(self.ports):
            text_name = self.__create_ports_label(port)
            x, y = self.__get_port_pos(port)
            logging.debug(r"Porta {i+1}: label={getattr(port, 'label', None)}, type={getattr(port, 'type', None)}, is_input={port.is_input()}, x={x}, y={y}")
            if port.is_input():
                alignment = Pango.Alignment.LEFT
                anchor = GooCanvas.CanvasAnchorType.WEST
            else:
                alignment = Pango.Alignment.RIGHT
                anchor = GooCanvas.CanvasAnchorType.EAST
            press_event = self.__on_input_press if port.is_input() else self.__on_output_press
            release_event = self.__on_input_release if port.is_input() else self.__on_output_release

            text = GooCanvas.CanvasText(parent=self,
                                 text=text_name,
                                 fill_color='black',
                                 anchor=anchor,
                                 alignment=alignment,
                                 x=x,
                                 y=y,
                                 use_markup=True,
                                 tooltip=port.label
                                 )
            text.connect("button-press-event", press_event, port)
            text.connect("button-release-event", release_event, port)
            self.widgets["port" + str(port)] = text
            logging.debug(r"Porta {i+1} criada com sucesso: anchor={anchor}, alignment={alignment}")

    # ----------------------------------------------------------------------
    def __on_input_press(self, canvas_item: Any, target_item: Any, event: Gdk.Event, port: Port) -> bool:
        """
        This method return true if a input was connected.

            Parameters:
                * **canvas_item**
                * **target_item**
                * **event**
            Returns:
                * **Types** (:class:`boolean<boolean>`): Indicates the input as connected.
        """
        self.diagram.end_connection(self, port)
        return True

    # ----------------------------------------------------------------------
    def __on_input_release(self, canvas_item: Any, target_item: Any, event: Gdk.Event, args: Any) -> bool:
        """
        This method monitors the input release.

            Parameters:
                * **canvas_item**
                * **target_item**
                * **event **
            Return:
                * **Types** (:class:`boolean<boolean>`)
        """
        return True

    # ----------------------------------------------------------------------
    def __on_output_press(self, canvas_item: Any, target_item: Any, event: Gdk.Event, port: Port) -> bool:
        """
        This method monitors the output state, monitors if output was pressed.

            Parameters:
                canvas_item
                target_item
                event
                args
            Returns:
                * **Types** (:class:`boolean<boolean>`)
        """
        self.diagram.start_connection(self, port)
        return True

    # ----------------------------------------------------------------------
    def __on_output_release(self, canvas_item: Any, target_item: Any, event: Gdk.Event, args: Any) -> bool:
        """
        This method monitors the output state, monitors if output was release.

            Returns:
                * **Types** (:class:`boolean<boolean>`)
        """
        return True

    # ----------------------------------------------------------------------
    def __get_port_pos(self, port: Port) -> Tuple[int, int]:
        if self.is_collapsed:
            y = 16 + (port.type_index * 6)
        else:
            y = 26 + (port.type_index * 11)
 
        if port.is_input():
            x = 0
        else:
            x = self.width
 
        if not self.is_collapsed:
            return (x, y)
 
        if port.is_input():
            return (x + 36, y - 8)
        else:
            return (x - 25, y - 8)

    # ----------------------------------------------------------------------
    def get_port_pos(self, port: Port) -> Tuple[float, float]:
        """
        This method get input position.

            Parameters:
                * **input_id**
            Returns:
                * **Types** (:class:`float<float>`)
        """
        x, y = self.get_position()
        x2, y2 = self.__get_port_pos(port)
        return x + x2, y + y2 + 1

    # ----------------------------------------------------------------------
    def __calculate_height(self) -> int:
        if self.is_collapsed:
            return max(((self.maxIO - 1) * 5) + (self.maxIO * 4), 40)
        else:
            return max(((self.maxIO) * 5) + 15 + (self.maxIO * 7), 50)

    # ----------------------------------------------------------------------
    def move(self, x: int, y: int) -> None:
        """
        This method move a block.

            Parameters:
                * **(x,y)** (:class:`float<float>`)
            Returns:
                * **Types** (:class:`float<float>`)
        """
        new_x = x - (x % System.get_preferences().grid)
        new_y = y - (y % System.get_preferences().grid)
        self.translate(new_x, new_y)

    # ----------------------------------------------------------------------
    def adjust_position(self) -> None:
        position = self.get_position()
        grid = System.get_preferences().grid
        new_x = position[0] - position[0] % grid
        new_y = position[1] - position[1] % grid
        self.translate(new_x - position[0], new_y - position[1])

    # ----------------------------------------------------------------------
    def get_position(self) -> Tuple[float, float]:
        """
        This method get position the block.

             Returns:
                * **Types** (:class:`float<float>`)
        """
        isSet, x, y, scale, rotation = self.get_simple_transform()
        return x, y

    # ----------------------------------------------------------------------
    def set_properties(self, data: Any) -> None:
        """
        This method set properties of each block.

            Parameters:
                * **data**
        """
        BlockModel.set_properties(self, data)

    # ----------------------------------------------------------------------
    def get_properties(self) -> Any:
        """
        This method get properties of each block.

            Returns:
                * **Types** ()
        """
        return BlockModel.get_properties(self)

    # ----------------------------------------------------------------------
    def update_flow(self) -> bool:
        """
        This method update flow.

            Returns:
                * **Types** (:class:`boolean<boolean>`)
        """
        self.has_flow = True
        distinct_con = []
        for conn in self.diagram.connectors:
            if conn.input != self:
                continue
            if conn.input_port not in distinct_con:
                distinct_con.append(conn.input_port)
        in_count = 0
        for port in self.ports:
            if port.is_input():
                in_count += 1
        if len(distinct_con) < in_count:
            self.has_flow = False
        self.__update_state()
        return self.has_flow

    # ----------------------------------------------------------------------
    def __update_state(self) -> None:
        """
        This method update the Line state.
        """
        # Not connected: Color = red
        if self.has_flow:
            self.widgets["Rect"].set_property("stroke_color", 'black')
        else:
            self.widgets["Rect"].set_property("stroke_color", 'red')

        # in focus: Line width = 3
        if self.focus:
            self.widgets["Rect"].set_property("line-width", 3)
        else:
            self.widgets["Rect"].set_property("line-width", 1)

        # selected: Line = dashed
        if self.is_selected:
            self.widgets["Rect"].set_property(
                "line_dash", GooCanvas.CanvasLineDash.newv((4.0, 2.0)))
        else:
            self.widgets["Rect"].set_property(
                "line_dash", GooCanvas.CanvasLineDash.newv((10.0, 0.0)))

        self.height = self.__calculate_height()

        if self.is_collapsed:
            self.widgets["Label"].set_property("visibility", GooCanvas.CanvasItemVisibility.INVISIBLE)
            self.widgets["Rect"].set_property("width", self.width - 60)
            self.widgets["Rect"].set_property("x", 35)
            self.widgets["Rect"].set_property("y", 0)
            self.widgets["Rect"].set_property("height", self.height - 10)
            self.widgets["Icon"].set_property("y", (self.height - 10)/2)
            self.widgets["Icon"].set_property("x", (self.width / 2) + 2)
            for port in self.ports:
                x,y = self.__get_port_pos(port)
                if "port" + str(port) in self.widgets:
                    self.widgets["port" + str(port)].set_property("x", x)
                    self.widgets["port" + str(port)].set_property("y", y)
                    self.widgets["port" + str(port)].set_property("text", self.__create_ports_label(port))
            return True

        if not self.is_collapsed:
            self.widgets["Label"].set_property("visibility", GooCanvas.CanvasItemVisibility.VISIBLE)
            self.widgets["Rect"].set_property("width", self.width)
            self.widgets["Rect"].set_property("x", 0)
            self.widgets["Rect"].set_property("y", 10)
            self.widgets["Rect"].set_property("height", self.height)
            self.widgets["Icon"].set_property("y", (self.height + 20)/2)
            self.widgets["Icon"].set_property("x", (self.width / 2))
            for port in self.ports:
                x,y = self.__get_port_pos(port)
                if "port" + str(port) in self.widgets:
                    self.widgets["port" + str(port)].set_property("x", x)
                    self.widgets["port" + str(port)].set_property("y", y)
                    self.widgets["port" + str(port)].set_property("text", self.__create_ports_label(port))

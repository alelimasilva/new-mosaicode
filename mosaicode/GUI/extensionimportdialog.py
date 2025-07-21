import gi
import threading
from typing import List, Dict

try:
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
except (ImportError, ValueError):
    raise ImportError('GTK 3.0 não está disponível. Instale o pacote python3-gi e libgtk-3-dev.')

class ExtensionImportDialog(Gtk.Dialog):
    def __init__(self, parent, extensions: List[Dict[str, str]]):
        super().__init__(title="Importar Extensões Disponíveis", transient_for=parent, flags=0)
        self.set_default_size(500, 350)
        self.set_modal(True)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            "Importar Selecionadas", Gtk.ResponseType.OK
        )

        self.selected = set()
        self.extensions = extensions

        box = self.get_content_area()
        label = Gtk.Label(label="Selecione as extensões que deseja importar:")
        box.add(label)

        # Criar ListStore: checkbox, nome, data, tamanho
        self.store = Gtk.ListStore(bool, str, str, str)
        for ext in sorted(extensions, key=lambda x: x['name'].lower()):
            self.store.append([False, ext['name'], ext['date'], ext['size']])

        treeview = Gtk.TreeView(model=self.store)
        # Checkbox
        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_toggle)
        col_toggle = Gtk.TreeViewColumn("Selecionar", renderer_toggle, active=0)
        treeview.append_column(col_toggle)
        # Nome
        renderer_text = Gtk.CellRendererText()
        col_name = Gtk.TreeViewColumn("Nome", renderer_text, text=1)
        treeview.append_column(col_name)
        # Data
        renderer_date = Gtk.CellRendererText()
        col_date = Gtk.TreeViewColumn("Data", renderer_date, text=2)
        treeview.append_column(col_date)
        # Tamanho
        renderer_size = Gtk.CellRendererText()
        col_size = Gtk.TreeViewColumn("Tamanho", renderer_size, text=3)
        treeview.append_column(col_size)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.add(treeview)
        box.add(scrolled)
        self.show_all()

    def on_toggle(self, widget, path):
        self.store[path][0] = not self.store[path][0]

    def get_selected_extensions(self) -> List[str]:
        return [row[1] for row in self.store if row[0]]

    def get_selected_files(self):
        """Retorna uma lista com os nomes dos arquivos selecionados."""
        return [row[1] for row in self.store if row[0]] 
# -*- coding: utf-8 -*-
"""
Enhanced Save Dialog that always asks user for save location.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import gettext
from typing import Optional, Any
from pathlib import Path

_ = gettext.gettext

class EnhancedSaveDialog(Gtk.FileChooserDialog):
    """
    Enhanced save dialog that always asks user for save location.
    """

    def __init__(self, main_window, title="Save", filetype=None):
        """
        Initialize the enhanced save dialog.
        
        Args:
            main_window: The main window
            title: Dialog title
            filetype: File type filter
        """
        Gtk.FileChooserDialog.__init__(
            self,
            title=title,
            transient_for=main_window,
            action=Gtk.FileChooserAction.SAVE,
            destroy_with_parent=True)
        
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_buttons(Gtk.STOCK_SAVE, Gtk.ResponseType.OK)

        # No default filename - user must choose
        self.set_current_name("")

        # Add file filters
        allfiles = Gtk.FileFilter()
        allfiles.set_name(_("All Files"))
        allfiles.add_pattern("*.*")
        self.add_filter(allfiles)

        if filetype is not None:
            filefilter = Gtk.FileFilter()
            filefilter.set_name(filetype)
            filefilter.add_pattern(f"*.{filetype}")
            self.add_filter(filefilter)

        self.show_all()

    def run(self) -> Optional[str]:
        """
        Run the dialog and return the selected path.
        
        Returns:
            Selected file path or None if cancelled
        """
        response = super(Gtk.FileChooserDialog, self).run()
        file_name = None
        if response == Gtk.ResponseType.OK:
            file_name = self.get_filename()
        self.close()
        self.destroy()
        return file_name

class EnhancedDirectoryDialog(Gtk.FileChooserDialog):
    """
    Enhanced directory selection dialog.
    """

    def __init__(self, main_window, title="Select Directory"):
        """
        Initialize the enhanced directory dialog.
        
        Args:
            main_window: The main window
            title: Dialog title
        """
        Gtk.FileChooserDialog.__init__(
            self,
            title=title,
            transient_for=main_window,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
            destroy_with_parent=True)
        
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_buttons(Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

        self.show_all()

    def run(self) -> Optional[str]:
        """
        Run the dialog and return the selected directory.
        
        Returns:
            Selected directory path or None if cancelled
        """
        response = super(Gtk.FileChooserDialog, self).run()
        directory = None
        if response == Gtk.ResponseType.OK:
            directory = self.get_filename()
        self.close()
        self.destroy()
        return directory
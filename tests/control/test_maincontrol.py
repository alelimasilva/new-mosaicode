# -*- coding: utf-8 -*-
"""
Tests for MainControl class.
Migrated from unittest to pytest.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile
import os

from mosaicode.control.maincontrol import MainControl
from mosaicode.model.blockmodel import BlockModel
from mosaicode.model.codetemplate import CodeTemplate
from mosaicode.model.port import Port
from mosaicode.model.commentmodel import CommentModel
from mosaicode.GUI.diagram import Diagram


@pytest.fixture
def mock_main_window():
    """Create a mock main window for testing."""
    mock_window = Mock()
    mock_window.menu = Mock()
    mock_window.block_notebook = Mock()
    mock_window.work_area = Mock()
    mock_window.status = Mock()
    
    # Mock Diagram class to avoid isinstance issues
    with patch('mosaicode.control.maincontrol.Diagram') as mock_diagram_class:
        mock_diagram_instance = Mock()
        mock_diagram_class.return_value = mock_diagram_instance
        yield mock_window


@pytest.fixture
def main_control(mock_main_window):
    """Create MainControl instance for testing."""
    control = MainControl(mock_main_window)
    control.init()
    control.new()
    return control


@pytest.fixture
def test_block():
    """Create a test block for testing."""
    block = BlockModel()
    block.type = "TestBlock"
    block.label = "Test Block"
    block.color = "#FF0000"
    block.group = "Test"
    return block


@pytest.fixture
def test_code_template():
    """Create a test code template for testing."""
    template = CodeTemplate()
    template.name = "TestTemplate"
    template.language = "python"
    template.command = "python"
    return template


@pytest.fixture
def test_port():
    """Create a test port for testing."""
    port = Port()
    port.name = "test_port"
    port.label = "Test Port"
    port.type = "Input"
    port.conn_type = Port.INPUT
    return port


def test_init(mock_main_window):
    """Test MainControl initialization."""
    control = MainControl(mock_main_window)
    control.init()
    
    # Verify that init calls the expected methods
    mock_main_window.menu.update_recent_files.assert_called_once()
    mock_main_window.menu.update_examples.assert_called_once()


def test_new(mock_main_window):
    """Test creating new diagram."""
    control = MainControl(mock_main_window)
    control.new()
    
    # Verify that add_diagram was called
    mock_main_window.work_area.add_diagram.assert_called_once()


@patch('mosaicode.control.maincontrol.OpenDialog')
def test_select_open_success(mock_open_dialog, main_control):
    """Test opening a file through dialog."""
    # Mock the dialog to return a filename
    mock_dialog_instance = Mock()
    mock_dialog_instance.run.return_value = "/path/to/test.mscd"
    mock_open_dialog.return_value = mock_dialog_instance
    
    main_control.select_open()
    
    # Verify dialog was created and run
    mock_open_dialog.assert_called_once()
    mock_dialog_instance.run.assert_called_once()


@patch('mosaicode.control.maincontrol.OpenDialog')
def test_select_open_cancelled(mock_open_dialog, main_control):
    """Test opening a file when dialog is cancelled."""
    # Mock the dialog to return None (cancelled)
    mock_dialog_instance = Mock()
    mock_dialog_instance.run.return_value = None
    mock_open_dialog.return_value = mock_dialog_instance
    
    main_control.select_open()
    
    # Verify dialog was created and run, but no further action
    mock_open_dialog.assert_called_once()
    mock_dialog_instance.run.assert_called_once()


@patch('mosaicode.control.maincontrol.DiagramControl')
def test_open_success(mock_diagram_control, main_control):
    """Test opening a file successfully."""
    # Mock successful load
    mock_control_instance = Mock()
    mock_control_instance.load.return_value = True
    mock_diagram_control.return_value = mock_control_instance
    
    main_control.open("/path/to/test.mscd")
    
    # Verify diagram was added and loaded
    mock_diagram_control.assert_called_once()
    mock_control_instance.load.assert_called_once_with("/path/to/test.mscd")


@patch('mosaicode.control.maincontrol.DiagramControl')
def test_open_failure(mock_diagram_control, main_control):
    """Test opening a file with load failure."""
    # Mock failed load
    mock_control_instance = Mock()
    mock_control_instance.load.return_value = False
    mock_diagram_control.return_value = mock_control_instance
    
    main_control.open("/path/to/test.mscd")
    
    # Verify diagram was added but load failed
    mock_diagram_control.assert_called_once()
    mock_control_instance.load.assert_called_once_with("/path/to/test.mscd")


def test_close(main_control):
    """Test closing current tab."""
    main_control.close()
    
    # Verify close_tab was called
    main_control.main_window.work_area.close_tab.assert_called_once()


@patch('mosaicode.control.maincontrol.SaveDialog')
@patch('mosaicode.control.maincontrol.ConfirmDialog')
@patch('mosaicode.control.maincontrol.DiagramControl')
@patch('mosaicode.control.maincontrol.MessageDialog')
def test_save_success(mock_message_dialog, mock_diagram_control, mock_confirm_dialog, mock_save_dialog, main_control):
    """Test saving diagram successfully."""
    # Mock current diagram
    mock_diagram = Mock()
    mock_diagram.file_name = None
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    
    # Mock save dialog
    mock_dialog_instance = Mock()
    mock_dialog_instance.run.return_value = "/path/to/test.mscd"
    mock_save_dialog.return_value = mock_dialog_instance
    
    # Mock successful save
    mock_control_instance = Mock()
    mock_control_instance.save.return_value = (True, "")
    mock_diagram_control.return_value = mock_control_instance
    
    result = main_control.save()
    
    assert result is True
    assert mock_diagram.file_name == "/path/to/test.mscd"


@patch('mosaicode.control.maincontrol.SaveDialog')
def test_save_no_diagram(mock_save_dialog, main_control):
    """Test saving when no diagram is current."""
    # Mock no current diagram
    main_control.main_window.work_area.get_current_diagram.return_value = None
    
    result = main_control.save()
    
    assert result is False
    mock_save_dialog.assert_not_called()


@patch('mosaicode.control.maincontrol.SaveDialog')
def test_save_cancelled(mock_save_dialog, main_control):
    """Test saving when dialog is cancelled."""
    # Mock current diagram
    mock_diagram = Mock()
    mock_diagram.file_name = None
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    
    # Mock save dialog cancelled
    mock_dialog_instance = Mock()
    mock_dialog_instance.run.return_value = None
    mock_save_dialog.return_value = mock_dialog_instance
    
    result = main_control.save()
    
    assert result is False


def test_save_as(main_control):
    """Test save as functionality."""
    with patch.object(main_control, 'save') as mock_save:
        main_control.save_as()
        mock_save.assert_called_once_with(save_as=True)


def test_save_as_example(main_control):
    """Test save as example functionality."""
    # Mock current diagram
    mock_diagram = Mock()
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    
    with patch('mosaicode.control.maincontrol.SaveDialog') as mock_save_dialog:
        mock_dialog_instance = Mock()
        mock_dialog_instance.run.return_value = "/path/to/example"
        mock_save_dialog.return_value = mock_dialog_instance
        
        with patch('mosaicode.control.maincontrol.DiagramControl') as mock_diagram_control:
            mock_control_instance = Mock()
            mock_control_instance.save.return_value = (True, "")
            mock_diagram_control.return_value = mock_control_instance
            
            main_control.save_as_example()
            
            mock_control_instance.save.assert_called_once()


def test_export_diagram(main_control):
    """Test diagram export functionality."""
    # Mock current diagram
    mock_diagram = Mock()
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    
    with patch('mosaicode.control.maincontrol.SaveDialog') as mock_save_dialog:
        mock_dialog_instance = Mock()
        mock_dialog_instance.run.return_value = "/path/to/export"
        mock_save_dialog.return_value = mock_dialog_instance
        
        with patch('mosaicode.control.maincontrol.DiagramControl') as mock_diagram_control:
            mock_control_instance = Mock()
            mock_control_instance.export.return_value = True
            mock_diagram_control.return_value = mock_control_instance
            
            result = main_control.export_diagram()
            
            assert result is True


def test_exit(main_control):
    """Test exit functionality."""
    with patch('mosaicode.control.maincontrol.Gtk.main_quit') as mock_quit:
        main_control.exit()
        mock_quit.assert_called_once()


def test_set_recent_files(main_control):
    """Test setting recent files."""
    main_control.set_recent_files("/path/to/test.mscd")
    
    # Verify recent files were updated
    main_control.main_window.menu.update_recent_files.assert_called()


def test_get_clipboard(main_control):
    """Test getting clipboard content."""
    # Add some items to clipboard
    main_control.clipboard = ["item1", "item2"]
    
    result = main_control.get_clipboard()
    
    assert result == ["item1", "item2"]


def test_reset_clipboard(main_control):
    """Test resetting clipboard."""
    # Add some items to clipboard
    main_control.clipboard = ["item1", "item2"]
    
    main_control.reset_clipboard()
    
    assert main_control.clipboard == []


def test_preferences(main_control):
    """Test opening preferences."""
    with patch('mosaicode.control.maincontrol.PreferenceWindow') as mock_pref_window:
        mock_window_instance = Mock()
        mock_pref_window.return_value = mock_window_instance
        
        main_control.preferences()
        
        mock_pref_window.assert_called_once()
        mock_window_instance.run.assert_called_once()


def test_about(main_control):
    """Test opening about dialog."""
    with patch('mosaicode.control.maincontrol.About') as mock_about:
        mock_about_instance = Mock()
        mock_about.return_value = mock_about_instance
        
        main_control.about()
        
        mock_about.assert_called_once()
        mock_about_instance.run.assert_called_once()


def test_search(main_control):
    """Test search functionality."""
    # Mock current diagram
    mock_diagram = Mock()
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    
    main_control.search("test query")
    
    # Verify search was called on diagram
    mock_diagram.search.assert_called_once_with("test query")


def test_set_block(main_control, test_block):
    """Test setting block."""
    # Mock current diagram
    mock_diagram = Mock()
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    
    main_control.set_block(test_block)
    
    # Verify block was set on diagram
    mock_diagram.set_block.assert_called_once_with(test_block)


def test_get_selected_block(main_control, test_block):
    """Test getting selected block."""
    # Mock current diagram
    mock_diagram = Mock()
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    mock_diagram.get_selected_block.return_value = test_block
    
    result = main_control.get_selected_block()
    
    assert result == test_block
    mock_diagram.get_selected_block.assert_called_once()


def test_clear_console(main_control):
    """Test clearing console."""
    main_control.clear_console()
    
    # Verify console was cleared
    main_control.main_window.status.clear.assert_called_once()


def test_add_block(main_control, test_block):
    """Test adding a block."""
    # Mock current diagram
    mock_diagram = Mock()
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    mock_block_widget = Mock()
    mock_diagram.add_block.return_value = mock_block_widget
    
    result = main_control.add_block(test_block)
    
    assert result == mock_block_widget
    mock_diagram.add_block.assert_called_once_with(test_block)


def test_add_comment(main_control):
    """Test adding a comment."""
    # Mock current diagram
    mock_diagram = Mock()
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    mock_comment_widget = Mock()
    mock_diagram.add_comment.return_value = mock_comment_widget
    
    result = main_control.add_comment()
    
    assert result == mock_comment_widget
    mock_diagram.add_comment.assert_called_once()


def test_select_all(main_control):
    """Test selecting all elements."""
    # Mock current diagram
    mock_diagram = Mock()
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    
    main_control.select_all()
    
    # Verify select_all was called on diagram
    mock_diagram.select_all.assert_called_once()


def test_cut(main_control):
    """Test cut functionality."""
    # Mock current diagram
    mock_diagram = Mock()
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    
    main_control.cut()
    
    # Verify cut was called on diagram
    mock_diagram.cut.assert_called_once()


def test_copy(main_control):
    """Test copy functionality."""
    # Mock current diagram
    mock_diagram = Mock()
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    
    main_control.copy()
    
    # Verify copy was called on diagram
    mock_diagram.copy.assert_called_once()


def test_paste(main_control):
    """Test paste functionality."""
    # Mock current diagram
    mock_diagram = Mock()
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    
    main_control.paste()
    
    # Verify paste was called on diagram
    mock_diagram.paste.assert_called_once()


def test_delete(main_control):
    """Test delete functionality."""
    # Mock current diagram
    mock_diagram = Mock()
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    
    main_control.delete()
    
    # Verify delete was called on diagram
    mock_diagram.delete.assert_called_once()


def test_zoom_in(main_control):
    """Test zoom in functionality."""
    # Mock current diagram
    mock_diagram = Mock()
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    
    main_control.zoom_in()
    
    # Verify zoom_in was called on diagram
    mock_diagram.zoom_in.assert_called_once()


def test_zoom_out(main_control):
    """Test zoom out functionality."""
    # Mock current diagram
    mock_diagram = Mock()
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    
    main_control.zoom_out()
    
    # Verify zoom_out was called on diagram
    mock_diagram.zoom_out.assert_called_once()


def test_zoom_normal(main_control):
    """Test zoom normal functionality."""
    # Mock current diagram
    mock_diagram = Mock()
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    
    main_control.zoom_normal()
    
    # Verify zoom_normal was called on diagram
    mock_diagram.zoom_normal.assert_called_once()


def test_undo(main_control):
    """Test undo functionality."""
    # Mock current diagram
    mock_diagram = Mock()
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    
    main_control.undo()
    
    # Verify undo was called on diagram
    mock_diagram.undo.assert_called_once()


def test_redo(main_control):
    """Test redo functionality."""
    # Mock current diagram
    mock_diagram = Mock()
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    
    main_control.redo()
    
    # Verify redo was called on diagram
    mock_diagram.redo.assert_called_once()


def test_align_top(main_control):
    """Test align top functionality."""
    # Mock current diagram
    mock_diagram = Mock()
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    
    main_control.align_top()
    
    # Verify align_top was called on diagram
    mock_diagram.align_top.assert_called_once()


def test_align_bottom(main_control):
    """Test align bottom functionality."""
    # Mock current diagram
    mock_diagram = Mock()
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    
    main_control.align_bottom()
    
    # Verify align_bottom was called on diagram
    mock_diagram.align_bottom.assert_called_once()


def test_align_left(main_control):
    """Test align left functionality."""
    # Mock current diagram
    mock_diagram = Mock()
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    
    main_control.align_left()
    
    # Verify align_left was called on diagram
    mock_diagram.align_left.assert_called_once()


def test_align_right(main_control):
    """Test align right functionality."""
    # Mock current diagram
    mock_diagram = Mock()
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    
    main_control.align_right()
    
    # Verify align_right was called on diagram
    mock_diagram.align_right.assert_called_once()


def test_collapse_all(main_control):
    """Test collapse all functionality."""
    # Mock current diagram
    mock_diagram = Mock()
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    
    main_control.collapse_all()
    
    # Verify collapse_all was called on diagram
    mock_diagram.collapse_all.assert_called_once()


def test_uncollapse_all(main_control):
    """Test uncollapse all functionality."""
    # Mock current diagram
    mock_diagram = Mock()
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    
    main_control.uncollapse_all()
    
    # Verify uncollapse_all was called on diagram
    mock_diagram.uncollapse_all.assert_called_once()


def test_redraw(main_control):
    """Test redraw functionality."""
    # Mock current diagram
    mock_diagram = Mock()
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    
    main_control.redraw(True)
    
    # Verify redraw was called on diagram
    mock_diagram.redraw.assert_called_once_with(True)


def test_toggle_grid(main_control):
    """Test toggle grid functionality."""
    # Mock current diagram
    mock_diagram = Mock()
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    
    main_control.toggle_grid()
    
    # Verify toggle_grid was called on diagram
    mock_diagram.toggle_grid.assert_called_once()


def test_add_extension_block(main_control, test_block):
    """Test adding block extension."""
    with patch('mosaicode.persistence.blockpersistence.BlockPersistence.save') as mock_save:
        main_control.add_extension(test_block)
        mock_save.assert_called_once()


def test_add_extension_code_template(main_control, test_code_template):
    """Test adding code template extension."""
    with patch('mosaicode.persistence.codetemplatepersistence.CodeTemplatePersistence.save') as mock_save:
        main_control.add_extension(test_code_template)
        mock_save.assert_called_once()


def test_add_extension_port(main_control, test_port):
    """Test adding port extension."""
    with patch('mosaicode.persistence.portpersistence.PortPersistence.save') as mock_save:
        main_control.add_extension(test_port)
        mock_save.assert_called_once()


def test_delete_extension_block(main_control, test_block):
    """Test deleting block extension."""
    with patch('mosaicode.persistence.blockpersistence.BlockPersistence.delete') as mock_delete:
        main_control.delete_extension(test_block.type, test_block)
        mock_delete.assert_called_once_with(test_block.type)


def test_delete_extension_code_template(main_control, test_code_template):
    """Test deleting code template extension."""
    with patch('mosaicode.persistence.codetemplatepersistence.CodeTemplatePersistence.delete') as mock_delete:
        main_control.delete_extension(test_code_template.name, test_code_template)
        mock_delete.assert_called_once_with(test_code_template.name)


def test_delete_extension_port(main_control):
    """Test deleting port extension."""
    with patch('mosaicode.persistence.portpersistence.PortPersistence.delete') as mock_delete:
        main_control.delete_extension("port_key", "port")
        mock_delete.assert_called_once_with("port_key")


def test_update_blocks(main_control):
    """Test updating blocks."""
    main_control.update_blocks()
    
    # Verify blocks were updated
    main_control.main_window.menu.update_blocks.assert_called_once()
    main_control.main_window.block_notebook.update_blocks.assert_called_once()


def test_update_all(main_control):
    """Test updating all components."""
    main_control.update_all()
    
    # Verify update_blocks was called
    main_control.main_window.menu.update_blocks.assert_called()
    main_control.main_window.block_notebook.update_blocks.assert_called()


def test_stop(main_control):
    """Test stopping execution."""
    mock_process = Mock()
    main_control.threads["test_thread"] = mock_process
    
    main_control.stop(None, mock_process)
    
    # Verify process was terminated
    mock_process.terminate.assert_called_once()


def test_view_source(main_control):
    """Test viewing source code."""
    # Mock current diagram
    mock_diagram = Mock()
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    
    with patch('mosaicode.control.maincontrol.CodeWindow') as mock_code_window:
        mock_window_instance = Mock()
        mock_code_window.return_value = mock_window_instance
        
        result = main_control.view_source()
        
        assert result is True
        mock_code_window.assert_called_once()


def test_save_source(main_control):
    """Test saving source code."""
    # Mock current diagram
    mock_diagram = Mock()
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    
    with patch.object(main_control, '_get_code_generator') as mock_get_generator:
        mock_generator = Mock()
        mock_get_generator.return_value = mock_generator
        mock_generator.generate.return_value = {"test.py": "print('test')"}
        
        result = main_control.save_source()
        
        assert result is True


def test_run(main_control):
    """Test running diagram."""
    # Mock current diagram
    mock_diagram = Mock()
    main_control.main_window.work_area.get_current_diagram.return_value = mock_diagram
    
    with patch.object(main_control, '_get_code_generator') as mock_get_generator:
        mock_generator = Mock()
        mock_get_generator.return_value = mock_generator
        mock_generator.generate.return_value = {"test.py": "print('test')"}
        
        result = main_control.run()
        
        assert result is True


# Removed test_publish as method doesn't exist in MainControl


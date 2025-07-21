import os
import tempfile
from pathlib import Path


def get_file_path(filename):
    directory = Path(__file__).resolve().parent
    file_path = directory / filename
    return str(file_path.resolve())


def get_temp_file():
    """Gets the temporary file.

        :return: temporary file.
    """
    with tempfile.NamedTemporaryFile() as file:
        return file.name


def get_absolute_path_from_file(file_path):
    """
    Get absolute path from a file path.
    
    Args:
        file_path: Relative or absolute file path
        
    Returns:
        Absolute path as string
    """
    return str(Path(file_path).resolve())


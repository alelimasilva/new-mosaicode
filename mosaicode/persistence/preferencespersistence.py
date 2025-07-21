# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the PreferencesPersistence class.
"""
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any

from mosaicode.model.preferences import Preferences
from mosaicode.persistence.persistence import Persistence

logger = logging.getLogger(__name__)


class PreferencesPersistence:
    """
    This class contains methods related the PreferencesPersistence class.
    """

    # ----------------------------------------------------------------------
    @classmethod
    def load(cls, path: Path) -> Preferences:
        """
        This method loads the preference from JSON file.

        Returns:
            Preferences instance with loaded data
        """
        prefs = Preferences()
        file_name = path / f"{prefs.conf_file_path}.json"
        file_name = file_name.expanduser()
        
        if not file_name.exists():
            return prefs

        # load the preferences
        if not file_name.exists():
            return prefs

        data: Dict[str, Any] = {}
        try:
            with open(file_name, 'r', encoding='utf-8') as data_file:
                data = json.load(data_file)

            if data.get("data") != "PREFERENCES":
                logger.warning(f"Invalid preferences file format: {file_name}")
                return prefs

            prefs.author = data.get("author", "")
            prefs.license = data.get("license", "GPL 3.0")
            prefs.version = data.get("version", "0.0.1")  # Default version

            prefs.default_directory = data.get("default_directory", "")
            prefs.default_filename = data.get("default_filename", "%n")
            prefs.grid = int(data.get("grid", 10))
            prefs.width = int(data.get("width", 900))
            prefs.height = int(data.get("height", 500))
            prefs.hpaned_work_area = int(data.get("hpaned_work_area", 150))
            prefs.vpaned_bottom = int(data.get("vpaned_bottom", 450))
            prefs.vpaned_left = int(data.get("vpaned_left", 300))

            files = data.get("recent_files", [])
            for file_name in files:
                prefs.recent_files.append(file_name)

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            # Import System here to avoid circular import
            from mosaicode.system import System
            System.log(f"Problem loading preferences: {e}")
            logger.error(f"Error loading preferences from {file_name}: {e}")

        return prefs

    # ----------------------------------------------------------------------
    @classmethod
    def save(cls, prefs: Preferences, path: Path) -> bool:
        """
        This method save the preference in user space.

        Returns:
            True if successful, False otherwise
        """
        x = {
            'data': "PREFERENCES",
            'author': prefs.author,
            'license': prefs.license,
            'version': prefs.version,
            'default_directory': prefs.default_directory,
            'default_filename': prefs.default_filename,
            'grid': prefs.grid,
            'width': prefs.width,
            'height': prefs.height,
            'hpaned_work_area': prefs.hpaned_work_area,
            'vpaned_bottom': prefs.vpaned_bottom,
            'vpaned_left': prefs.vpaned_left,
            'recent_files': []
        }
        
        for key in prefs.recent_files:
            x['recent_files'].append(key)

        if not Persistence.create_dir(path):
            return False
        
        try:
            file_name = path / f"{prefs.conf_file_path}.json"
            with open(file_name, 'w', encoding='utf-8') as data_file:
                json.dump(x, data_file, indent=4, ensure_ascii=False)
            return True

        except (IOError, OSError) as e:
            logger.error(f"Error saving preferences to {file_name}: {e}")
            return False

# ----------------------------------------------------------------------


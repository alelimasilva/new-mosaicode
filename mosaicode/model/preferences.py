# -*- coding: utf-8 -*-
"""
This module contains the Preferences class.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any
from pathlib import Path

@dataclass
class Preferences:
    """
    This class contain the default preferences from mosaicode user.
    """
    
    # Configuration
    conf_file_path: str = "configuration"
    
    # Author information
    author: str = ""
    license: str = "GPL 3.0"
    version: str = field(default_factory=lambda: Preferences._get_version())
    
    # File management
    recent_files: List[str] = field(default_factory=list)
    default_directory: str = field(default_factory=lambda: Preferences._get_default_directory())
    default_filename: str = "%n"
    
    # Grid settings
    grid: int = 10
    
    # GUI dimensions
    width: int = 900
    height: int = 500
    hpaned_work_area: int = 150
    vpaned_bottom: int = 450
    vpaned_left: int = 300
    
    # Connection type
    connection: str = "Curve"
    
    @staticmethod
    def _get_version() -> str:
        from mosaicode.system import System
        return System.VERSION

    @staticmethod
    def _get_default_directory() -> str:
        from mosaicode.system import System
        return str(System.get_user_dir() / "code-gen")

    @classmethod
    def load_from_json(cls) -> 'Preferences':
        """
        Load preferences from JSON configuration file.
        
        Returns:
            Preferences instance with loaded data
        """
        from mosaicode.utils.config_loader import ConfigLoader
        
        # Load system defaults first
        config_data = ConfigLoader.load_config("preferences")
        
        # Load user-specific overrides
        user_config = ConfigLoader.load_user_config("preferences")
        config_data.update(user_config)
        
        # Create preferences instance with loaded data
        preferences = cls()
        
        # Update attributes from config data
        for key, value in config_data.items():
            if hasattr(preferences, key):
                setattr(preferences, key, value)
        
        return preferences

    def save_to_json(self) -> bool:
        """
        Save preferences to JSON configuration file.
        
        Returns:
            True if successful, False otherwise
        """
        from mosaicode.utils.config_loader import ConfigLoader
        
        # Convert dataclass to dictionary
        config_data = {
            "conf_file_path": self.conf_file_path,
            "author": self.author,
            "license": self.license,
            "version": self.version,
            "recent_files": self.recent_files,
            "default_directory": self.default_directory,
            "default_filename": self.default_filename,
            "grid": self.grid,
            "width": self.width,
            "height": self.height,
            "hpaned_work_area": self.hpaned_work_area,
            "vpaned_bottom": self.vpaned_bottom,
            "vpaned_left": self.vpaned_left,
            "connection": self.connection
        }
        
        return ConfigLoader.save_user_config("preferences", config_data)

    def __post_init__(self):
        if not self.default_directory:
            self.default_directory = Preferences._get_default_directory()
        if not self.version:
            self.version = Preferences._get_version()

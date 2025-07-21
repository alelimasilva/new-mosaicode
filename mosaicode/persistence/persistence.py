# -*- coding: utf-8 -*-
"""
This module contains the Persistence class.
"""
import json
import logging
from pathlib import Path
from typing import Any, Optional, Dict, List, TypeVar, Generic, Type

from mosaicode.utils.logger import get_logger

logger = get_logger(__name__)

T = TypeVar('T')


class Persistence:
    """
    This class contains methods related the Persistence class.
    """

    # ----------------------------------------------------------------------
    @classmethod
    def create_dir(cls, path) -> bool:
        """
        Create directory if it doesn't exist.
        
        Args:
            path: Path to create (can be string or Path object)
            
        Returns:
            True if directory exists or was created successfully, False otherwise
        """
        try:
            # Ensure path is a Path object
            if isinstance(path, str):
                path = Path(path)
            elif not isinstance(path, Path):
                logger.error(f"Invalid path type: {type(path)}")
                return False
                
            path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Directory created/verified: {path}")
            return True
        except Exception as e:
            logger.error(f"Error creating directory {path}: {e}")
            return False

    # ----------------------------------------------------------------------
    @classmethod
    def load(cls, file_name: str) -> Optional[Dict[str, Any]]:
        """
        This method loads data from JSON file.

        Args:
            file_name: Path to the file to load

        Returns:
            Loaded data dictionary or None if loading failed
        """
        try:
            with open(file_name, 'r', encoding='utf-8') as data_file:
                data: Dict[str, Any] = json.load(data_file)
            logger.debug(f"Loaded data from {file_name}")
            return data
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logger.error(f"Error loading data from {file_name}: {e}")
            return None

    # ----------------------------------------------------------------------
    @classmethod
    def save(cls, file_name: str, data: Dict[str, Any]) -> bool:
        """
        This method saves data to JSON file.

        Args:
            file_name: Path to the file to save
            data: Data to save

        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure directory exists
            file_path = Path(file_name)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_name, 'w', encoding='utf-8') as data_file:
                json.dump(data, data_file, indent=2, ensure_ascii=False)
            logger.debug(f"Saved data to {file_name}")
            return True
        except Exception as e:
            logger.error(f"Error saving data to {file_name}: {e}")
            return False

    # ----------------------------------------------------------------------
    @classmethod
    def load_all(cls, directory: str, file_pattern: str = "*.json") -> List[Dict[str, Any]]:
        """
        Load all files from a directory matching a pattern.

        Args:
            directory: Directory to search in
            file_pattern: File pattern to match

        Returns:
            List of loaded data dictionaries
        """
        results: List[Dict[str, Any]] = []
        dir_path = Path(directory)
        
        if not dir_path.exists():
            logger.warning(f"Directory does not exist: {directory}")
            return results
        
        for file_path in dir_path.glob(file_pattern):
            try:
                data = cls.load(str(file_path))
                if data is not None:
                    results.append(data)
                    logger.debug(f"Loaded {file_path}")
            except Exception as e:
                logger.error(f"Error loading {file_path}: {e}")
        
        logger.info(f"Loaded {len(results)} files from {directory}")
        return results

    # ----------------------------------------------------------------------
    @classmethod
    def save_all(cls, directory: str, data_list: List[Dict[str, Any]], 
                 filename_generator: Optional[Any] = None) -> bool:
        """
        Save multiple data objects to a directory.

        Args:
            directory: Directory to save to
            data_list: List of data dictionaries to save
            filename_generator: Function to generate filenames

        Returns:
            True if all saves successful, False otherwise
        """
        dir_path = Path(directory)
        dir_path.mkdir(parents=True, exist_ok=True)
        
        success_count = 0
        for i, data in enumerate(data_list):
            if filename_generator:
                filename = filename_generator(data, i)
            else:
                filename = f"item_{i}.json"
            
            file_path = dir_path / filename
            if cls.save(str(file_path), data):
                success_count += 1
        
        logger.info(f"Saved {success_count}/{len(data_list)} files to {directory}")
        return success_count == len(data_list)

    # ----------------------------------------------------------------------
    @classmethod
    def validate_data(cls, data: Dict[str, Any], required_fields: List[str]) -> bool:
        """
        Validate that data contains required fields.

        Args:
            data: Data dictionary to validate
            required_fields: List of required field names

        Returns:
            True if valid, False otherwise
        """
        if not isinstance(data, dict):
            logger.error("Data is not a dictionary")
            return False
        
        for field in required_fields:
            if field not in data:
                logger.error(f"Required field '{field}' is missing")
                return False
        
        return True

    # ----------------------------------------------------------------------
    @classmethod
    def merge_data(cls, base_data: Dict[str, Any], 
                   override_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge two data dictionaries, with override_data taking precedence.

        Args:
            base_data: Base data dictionary
            override_data: Override data dictionary

        Returns:
            Merged data dictionary
        """
        merged = base_data.copy()
        merged.update(override_data)
        return merged

    # ----------------------------------------------------------------------
    @classmethod
    def backup_file(cls, file_name: str, backup_suffix: str = ".backup") -> bool:
        """
        Create a backup of a file.

        Args:
            file_name: Path to the file to backup
            backup_suffix: Suffix for backup file

        Returns:
            True if backup successful, False otherwise
        """
        try:
            file_path = Path(file_name)
            if not file_path.exists():
                logger.warning(f"File does not exist: {file_name}")
                return False
            
            backup_path = file_path.with_suffix(file_path.suffix + backup_suffix)
            import shutil
            shutil.copy2(file_path, backup_path)
            logger.debug(f"Created backup: {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Error creating backup of {file_name}: {e}")
            return False

    # ----------------------------------------------------------------------
    @classmethod
    def restore_backup(cls, file_name: str, backup_suffix: str = ".backup") -> bool:
        """
        Restore a file from its backup.

        Args:
            file_name: Path to the file to restore
            backup_suffix: Suffix of backup file

        Returns:
            True if restore successful, False otherwise
        """
        try:
            file_path = Path(file_name)
            backup_path = file_path.with_suffix(file_path.suffix + backup_suffix)
            
            if not backup_path.exists():
                logger.warning(f"Backup file does not exist: {backup_path}")
                return False
            
            import shutil
            shutil.copy2(backup_path, file_path)
            logger.debug(f"Restored from backup: {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Error restoring backup of {file_name}: {e}")
            return False


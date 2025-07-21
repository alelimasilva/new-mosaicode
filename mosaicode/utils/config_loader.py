# -*- coding: utf-8 -*-
"""
This module contains the ConfigLoader class for loading JSON configurations.
"""
import json
import logging
from functools import lru_cache, cached_property
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

from mosaicode.exceptions import ConfigurationError, FileOperationError
from mosaicode.utils.logger import get_logger

logger = get_logger(__name__)


class ConfigLoader:
    """
    This class provides methods to load JSON configuration files with caching for performance.
    """

    # Schema definitions for validation
    PREFERENCES_SCHEMA = {
        "type": "object",
        "properties": {
            "author": {"type": "string"},
            "license": {"type": "string"},
            "version": {"type": "string"},
            "recent_files": {"type": "array", "items": {"type": "string"}},
            "grid": {"type": "integer", "minimum": 1, "maximum": 100},
            "width": {"type": "integer", "minimum": 100, "maximum": 3000},
            "height": {"type": "integer", "minimum": 100, "maximum": 3000},
            "default_directory": {"type": "string"},
            "default_filename": {"type": "string"},
            "connection": {"type": "string"}
        },
        "required": ["author", "license", "version"]
    }

    SYSTEM_SCHEMA = {
        "type": "object",
        "properties": {
            "app_name": {"type": "string"},
            "version": {"type": "string"},
            "zoom_levels": {
                "type": "object",
                "properties": {
                    "original": {"type": "integer"},
                    "in": {"type": "integer"},
                    "out": {"type": "integer"}
                }
            },
            "directories": {"type": "array", "items": {"type": "string"}},
            "file_extensions": {"type": "object"}
        },
        "required": ["app_name", "version"]
    }

    BLOCK_DEFAULTS_SCHEMA = {
        "type": "object",
        "properties": {
            "default_values": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "version": {"type": "string"},
                    "x": {"type": "integer"},
                    "y": {"type": "integer"},
                    "is_collapsed": {"type": "boolean"},
                    "language": {"type": "string"},
                    "extension": {"type": "string"},
                    "help": {"type": "string"},
                    "label": {"type": "string"},
                    "color": {"type": "string"},
                    "group": {"type": "string"},
                    "ports": {"type": "array"},
                    "maxIO": {"type": "integer"},
                    "properties": {"type": "array"}
                }
            }
        }
    }

    PORT_DEFAULTS_SCHEMA = {
        "type": "object",
        "properties": {
            "default_values": {
                "type": "object",
                "properties": {
                    "version": {"type": "string"},
                    "language": {"type": "string"},
                    "hint": {"type": "string"},
                    "color": {"type": "string"},
                    "multiple": {"type": "boolean"},
                    "code": {"type": "string"},
                    "var_name": {"type": "string"},
                    "conn_type": {"type": "string"},
                    "name": {"type": "string"},
                    "label": {"type": "string"},
                    "index": {"type": "integer"},
                    "type_index": {"type": "integer"}
                }
            }
        }
    }
    FIELD_DEFAULTS_SCHEMA = {
        "type": "object",
        "properties": {
            "field_types": {"type": "object"},
            "field_configurations": {"type": "object"}
        }
    }

    PERSISTENCE_DEFAULTS_SCHEMA = {
        "type": "object", 
        "properties": {
            "serialization_formats": {"type": "object"},
            "default_serialization": {"type": "object"}
        }
    }

    EXTENSION_DEFAULTS_SCHEMA = {
        "type": "object",
        "properties": {
            "extension_types": {"type": "object"},
            "extension_directories": {"type": "object"},
            "extension_validation": {"type": "object"}
        }
    }

    @cached_property
    def _user_config_dir(self) -> Path:
        """Cache the user configuration directory path."""
        from mosaicode.system import System
        return System.get_user_dir() / "config"

    @cached_property
    def _template_dir(self) -> Path:
        """Cache the template directory path."""
        from mosaicode.system import System
        return System.get_user_dir() / "templates"

    @staticmethod
    def validate_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
        """
        Validate JSON data against a schema with caching.
        
        Args:
            data: JSON data to validate
            schema: Schema definition
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Basic validation without external dependencies
            if not isinstance(data, dict):
                logger.error("Data is not a dictionary")
                return False
            
            # Check required fields
            required_fields = schema.get("required", [])
            for field in required_fields:
                if field not in data:
                    logger.error(f"Required field '{field}' is missing")
                    return False
            
            # Check properties
            properties = schema.get("properties", {})
            for field_name, field_value in data.items():
                if field_name in properties:
                    field_schema = properties[field_name]
                    if not ConfigLoader._validate_field(field_value, field_schema):
                        logger.error(f"Field '{field_name}' is invalid")
                        return False
            
            return True
            
        except Exception as e:
            logger.error(f"Schema validation error: {e}")
            return False

    @staticmethod
    def _validate_field(value: Any, schema: Dict[str, Any]) -> bool:
        """
        Validate a single field against its schema.
        
        Args:
            value: Field value to validate
            schema: Field schema definition
            
        Returns:
            True if valid, False otherwise
        """
        expected_type = schema.get("type")
        
        if expected_type == "string":
            if not isinstance(value, str):
                return False
        elif expected_type == "integer":
            if not isinstance(value, int):
                return False
        elif expected_type == "boolean":
            if not isinstance(value, bool):
                return False
        elif expected_type == "array":
            if not isinstance(value, list):
                return False
        elif expected_type == "object":
            if not isinstance(value, dict):
                return False
        
        # Check constraints
        if expected_type == "integer":
            min_value = schema.get("minimum")
            max_value = schema.get("maximum")
            if min_value is not None and value < min_value:
                return False
            if max_value is not None and value > max_value:
                return False
        
        return True

    @staticmethod
    @lru_cache(maxsize=16)
    def load_config(config_name: str, config_dir: Optional[Path] = None, validate: bool = True, use_pydantic: bool = False) -> Dict[str, Any]:
        """
        Load configuration from JSON file with caching for performance.
        
        Args:
            config_name: Name of the configuration file (without .json extension)
            config_dir: Directory containing config files (optional)
            validate: Whether to validate the loaded configuration
            use_pydantic: Whether to use Pydantic validation (if available)
            
        Returns:
            Dictionary containing the loaded configuration
            
        Raises:
            ConfigurationError: If configuration is invalid
            FileOperationError: If file operation fails
        """
        try:
            # Determine config directory
            if config_dir is None:
                from mosaicode.system import System
                config_dir = System.get_user_dir() / "config"
            
            # Build file path
            config_file = config_dir / f"{config_name}.json"
            
            if not config_file.exists():
                logger.warning(f"Configuration file not found: {config_file}")
                return {}
            
            # Load JSON data
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logger.debug(f"Loaded configuration from {config_file}")
            
            # Validate if requested
            if validate:
                schema = ConfigLoader._get_schema_for_config(config_name)
                if schema and not ConfigLoader.validate_schema(data, schema):
                    raise ConfigurationError(f"Invalid configuration format: {config_name}")
            
            return data
            
        except (json.JSONDecodeError, FileNotFoundError) as e:
            raise FileOperationError(f"Failed to load configuration {config_name}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error loading configuration {config_name}: {e}")
            return {}

    @staticmethod
    @lru_cache(maxsize=16)
    def load_template(template_name: str, template_type: str, validate: bool = True, use_pydantic: bool = False) -> Dict[str, Any]:
        """
        Load template from JSON file with caching for performance.
        
        Args:
            template_name: Name of the template file (without .json extension)
            template_type: Type of template (blocks, ports, fields, etc.)
            validate: Whether to validate the loaded template
            use_pydantic: Whether to use Pydantic validation (if available)
            
        Returns:
            Dictionary containing the loaded template
            
        Raises:
            ConfigurationError: If template is invalid
            FileOperationError: If file operation fails
        """
        try:
            # Determine template directory
            from mosaicode.system import System
            template_dir = System.get_user_dir() / "templates" / template_type
            
            # Build file path
            template_file = template_dir / f"{template_name}.json"
            
            if not template_file.exists():
                logger.warning(f"Template file not found: {template_file}")
                return {}
            
            # Load JSON data
            with open(template_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logger.debug(f"Loaded template from {template_file}")
            
            # Validate if requested
            if validate:
                schema = ConfigLoader._get_schema_for_template(template_type)
                if schema and not ConfigLoader.validate_schema(data, schema):
                    raise ConfigurationError(f"Invalid template format: {template_name}")
            
            return data
            
        except (json.JSONDecodeError, FileNotFoundError) as e:
            raise FileOperationError(f"Failed to load template {template_name}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error loading template {template_name}: {e}")
            return {}

    @staticmethod
    @lru_cache(maxsize=8)
    def _get_schema_for_config(config_name: str) -> Optional[Dict[str, Any]]:
        """
        Get schema for configuration with caching.
        
        Args:
            config_name: Name of the configuration
            
        Returns:
            Schema dictionary or None if not found
        """
        schemas = {
            "preferences": ConfigLoader.PREFERENCES_SCHEMA,
            "system": ConfigLoader.SYSTEM_SCHEMA
        }
        return schemas.get(config_name)

    @staticmethod
    @lru_cache(maxsize=8)
    def _get_schema_for_template(template_type: str) -> Optional[Dict[str, Any]]:
        """
        Get schema for template type with caching.
        
        Args:
            template_type: Type of template
            
        Returns:
            Schema dictionary or None if not found
        """
        schemas = {
            "blocks": ConfigLoader.BLOCK_DEFAULTS_SCHEMA,
            "ports": ConfigLoader.PORT_DEFAULTS_SCHEMA,
            "fields": ConfigLoader.FIELD_DEFAULTS_SCHEMA,
            "persistence": ConfigLoader.PERSISTENCE_DEFAULTS_SCHEMA,
            "extensions": ConfigLoader.EXTENSION_DEFAULTS_SCHEMA
        }
        return schemas.get(template_type)

    @staticmethod
    def save_config(config_name: str, config_data: Dict[str, Any], config_dir: Optional[Path] = None, validate: bool = True, use_pydantic: bool = False) -> bool:
        """
        Save configuration data to JSON file with optional validation.
        
        Args:
            config_name: Name of the configuration file (without .json extension)
            config_data: Dictionary containing the configuration data
            config_dir: Directory to save config files (defaults to mosaicode/config)
            validate: Whether to validate the configuration before saving
            use_pydantic: Whether to use Pydantic for advanced validation
            
        Returns:
            True if successful, False otherwise
        """
        if config_dir is None:
            config_dir = Path(__file__).parent.parent / "config"
        
        # Validate before saving if requested
        if validate:
            if use_pydantic:
                # Use Pydantic for advanced validation
                from mosaicode.utils.pydantic_schemas import PydanticValidator
                
                if config_name == "system":
                    result = PydanticValidator.validate_system_config(config_data)
                elif config_name == "preferences":
                    result = PydanticValidator.validate_preferences(config_data)
                else:
                    # Fallback to basic validation
                    schema = ConfigLoader._get_schema_for_config(config_name)
                    if schema and not ConfigLoader.validate_schema(config_data, schema):
                        logger.error(f"Configuration data failed validation before saving")
                        return False
                    result = None
                
                if result and not result.success:
                    logger.error(f"Configuration data failed Pydantic validation before saving: {', '.join(result.errors)}")
                    return False
            else:
                # Use basic validation
                schema = ConfigLoader._get_schema_for_config(config_name)
                if schema and not ConfigLoader.validate_schema(config_data, schema):
                    logger.error(f"Configuration data failed validation before saving")
                    return False
        
        config_path = config_dir / f"{config_name}.json"
        
        try:
            config_dir.mkdir(parents=True, exist_ok=True)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            logger.debug(f"Saved configuration to {config_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving configuration to {config_path}: {e}")
            return False

    @staticmethod
    def get_user_config_dir() -> Path:
        """
        Get the user configuration directory.
        
        Returns:
            Path to user configuration directory
        """
        from mosaicode.system import System
        user_dir = System.get_user_dir()
        config_dir = user_dir / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir

    @staticmethod
    def load_user_config(config_name: str, validate: bool = True, use_pydantic: bool = False) -> Dict[str, Any]:
        """
        Load user-specific configuration from JSON with optional validation.
        
        Args:
            config_name: Name of the configuration file (without .json extension)
            validate: Whether to validate the configuration against schema
            use_pydantic: Whether to use Pydantic for advanced validation
            
        Returns:
            Dictionary containing the user configuration data
        """
        user_config_dir = Path.home() / "mosaicode" / "config"
        user_config_path = user_config_dir / f"{config_name}.json"
        
        if not user_config_path.exists():
            logger.debug(f"User config file not found: {user_config_path}")
            return {}
        
        try:
            with open(user_config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Validate against schema if requested
            if validate:
                if use_pydantic:
                    # Use Pydantic for advanced validation
                    from mosaicode.utils.pydantic_schemas import PydanticValidator
                    
                    if config_name == "preferences":
                        result = PydanticValidator.validate_preferences(config_data)
                    else:
                        # Fallback to basic validation
                        schema = ConfigLoader._get_schema_for_config(config_name)
                        if schema and not ConfigLoader.validate_schema(config_data, schema):
                            logger.warning(f"User configuration {config_name}.json failed schema validation")
                            return {}
                        result = None
                    
                    if result and not result.success:
                        logger.warning(f"User configuration {config_name}.json failed Pydantic validation: {', '.join(result.errors)}")
                        return {}
                    
                    if result and result.data:
                        config_data = result.data
                else:
                    # Use basic validation
                    schema = ConfigLoader._get_schema_for_config(config_name)
                    if schema and not ConfigLoader.validate_schema(config_data, schema):
                        logger.warning(f"User configuration {config_name}.json failed schema validation")
                        return {}
            
            logger.debug(f"Loaded user configuration from {user_config_path}")
            return config_data
            
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON in user config {user_config_path}: {e}"
            logger.error(error_msg)
            raise ConfigurationError(error_msg, str(user_config_path))
        except Exception as e:
            error_msg = f"Error loading user configuration from {user_config_path}: {e}"
            logger.error(error_msg)
            raise FileOperationError(error_msg, str(user_config_path), "read")

    @staticmethod
    def save_user_config(config_name: str, config_data: Dict[str, Any], validate: bool = True, use_pydantic: bool = False) -> bool:
        """
        Save user-specific configuration to JSON with optional validation.
        
        Args:
            config_name: Name of the configuration file (without .json extension)
            config_data: Configuration data to save
            validate: Whether to validate the configuration before saving
            use_pydantic: Whether to use Pydantic for advanced validation
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            FileOperationError: If file operations fail
        """
        # Validate before saving if requested
        if validate:
            if use_pydantic:
                # Use Pydantic for advanced validation
                from mosaicode.utils.pydantic_schemas import PydanticValidator
                
                if config_name == "preferences":
                    result = PydanticValidator.validate_preferences(config_data)
                else:
                    # Fallback to basic validation
                    schema = ConfigLoader._get_schema_for_config(config_name)
                    if schema and not ConfigLoader.validate_schema(config_data, schema):
                        logger.error(f"User configuration data failed validation before saving")
                        return False
                    result = None
                
                if result and not result.success:
                    logger.error(f"User configuration data failed Pydantic validation before saving: {', '.join(result.errors)}")
                    return False
            else:
                # Use basic validation
                schema = ConfigLoader._get_schema_for_config(config_name)
                if schema and not ConfigLoader.validate_schema(config_data, schema):
                    logger.error(f"User configuration data failed validation before saving")
                    return False
        
        user_config_dir = Path.home() / "mosaicode" / "config"
        user_config_dir.mkdir(parents=True, exist_ok=True)
        user_config_path = user_config_dir / f"{config_name}.json"
        
        try:
            with open(user_config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4, ensure_ascii=False)
            logger.debug(f"Saved user configuration to {user_config_path}")
            return True
        except Exception as e:
            error_msg = f"Error saving user configuration to {user_config_path}: {e}"
            logger.error(error_msg)
            raise FileOperationError(error_msg, str(user_config_path), "write")

    @staticmethod
    def validate_all_configs(use_pydantic: bool = False) -> Dict[str, bool]:
        """
        Validate all configuration files in the system.
        
        Args:
            use_pydantic: Whether to use Pydantic for advanced validation
            
        Returns:
            Dictionary mapping config names to validation results
        """
        results = {}
        
        if use_pydantic:
            # Use Pydantic for advanced validation
            from mosaicode.utils.pydantic_schemas import PydanticValidator
            pydantic_results = PydanticValidator.validate_all_configs()
            
            for config_name, result in pydantic_results.items():
                results[config_name] = result.success
                if result.success:
                    logger.info(f"[OK] {config_name}.json validated successfully with Pydantic")
                else:
                    logger.error(f"[ERRO] {config_name}.json Pydantic validation failed: {', '.join(result.errors)}")
        else:
            # Use basic validation
            # Validate system configs
            config_dir = Path(__file__).parent.parent / "config"
            for config_file in config_dir.glob("*.json"):
                config_name = config_file.stem
                try:
                    config_data = ConfigLoader.load_config(config_name, validate=True, use_pydantic=False)
                    results[config_name] = True
                    logger.info(f"[OK] {config_name}.json validated successfully")
                except Exception as e:
                    results[config_name] = False
                    logger.error(f"[ERRO] {config_name}.json validation failed: {e}")
            
            # Validate templates
            templates_dir = Path(__file__).parent.parent / "templates"
            for template_type_dir in templates_dir.iterdir():
                if template_type_dir.is_dir():
                    for template_file in template_type_dir.glob("*.json"):
                        template_name = template_file.stem
                        template_type = template_type_dir.name
                        full_name = f"{template_type}/{template_name}"
                        try:
                            template_data = ConfigLoader.load_template(template_name, template_type, validate=True, use_pydantic=False)
                            results[full_name] = True
                            logger.info(f"[OK] {full_name}.json validated successfully")
                        except Exception as e:
                            results[full_name] = False
                            logger.error(f"[ERRO] {full_name}.json validation failed: {e}")
        
        return results 
# -*- coding: utf-8 -*-
"""
This module contains Pydantic schemas for advanced validation.
Implements Pydantic models for all configuration types.
"""
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from pydantic import BaseModel, Field, validator, root_validator
from pydantic.types import StrictStr, StrictInt, StrictBool

from mosaicode.utils.logger import get_logger

logger = get_logger(__name__)


class ZoomLevels(BaseModel):
    """Schema for zoom level configuration."""
    original: int = Field(default=1, ge=1, le=10, description="Original zoom level")
    zoom_in: int = Field(default=2, ge=1, le=10, description="Zoom in level")
    zoom_out: int = Field(default=3, ge=1, le=10, description="Zoom out level")
    
    @validator('zoom_in')
    def validate_zoom_in(cls, v, values):
        """Validate zoom_in is greater than original."""
        if 'original' in values and v <= values['original']:
            raise ValueError('zoom_in must be greater than original')
        return v
    
    @validator('zoom_out')
    def validate_zoom_out(cls, v, values):
        """Validate zoom_out is less than original."""
        if 'original' in values and v >= values['original']:
            raise ValueError('zoom_out must be less than original')
        return v


class FileExtensions(BaseModel):
    """Schema for file extensions configuration."""
    diagram: str = Field(default=".mscd", description="Diagram file extension")
    code_template: str = Field(default=".json", description="Code template file extension")
    port: str = Field(default=".json", description="Port file extension")
    
    @validator('*')
    def validate_extensions(cls, v):
        """Validate file extensions start with dot."""
        if not v.startswith('.'):
            raise ValueError('File extension must start with dot')
        return v


class SystemConfig(BaseModel):
    """Schema for system configuration."""
    app_name: str = Field(description="Application name")
    version: str = Field(description="Application version")
    zoom_levels: ZoomLevels = Field(default_factory=ZoomLevels, description="Zoom level configuration")
    directories: List[str] = Field(default_factory=lambda: ["extensions", "images", "code-gen"], description="System directories")
    file_extensions: FileExtensions = Field(default_factory=FileExtensions, description="File extensions configuration")
    extension_server_url: str = Field(default="https://alice.ufsj.edu.br/mosaicode/extensions/", description="Extension server URL")
    
    class Config:
        """Pydantic configuration."""
        extra = "forbid"  # Reject extra fields
        validate_assignment = True  # Validate on assignment


class Preferences(BaseModel):
    """Schema for user preferences."""
    conf_file_path: Optional[str] = Field(default="configuration", description="Configuration file path")
    author: str = Field(description="Author name")
    license: str = Field(description="License type")
    version: str = Field(description="Preferences version")
    recent_files: List[str] = Field(default_factory=list, description="List of recent files")
    grid: int = Field(default=10, ge=1, le=100, description="Grid size")
    width: int = Field(default=900, ge=100, le=3000, description="Window width")
    height: int = Field(default=500, ge=100, le=3000, description="Window height")
    default_directory: str = Field(default="~/mosaicode/code-gen", description="Default directory")
    default_filename: str = Field(default="%n", description="Default filename pattern")
    connection: str = Field(default="Curve", description="Connection type")
    hpaned_work_area: int = Field(default=150, ge=50, le=1000, description="Horizontal paned position")
    vpaned_bottom: int = Field(default=450, ge=50, le=1000, description="Vertical paned bottom position")
    vpaned_left: int = Field(default=300, ge=50, le=1000, description="Vertical paned left position")
    
    @validator('default_directory')
    def validate_default_directory(cls, v):
        """Validate default directory path."""
        if not v:
            raise ValueError('Default directory cannot be empty')
        return v
    
    @validator('default_filename')
    def validate_default_filename(cls, v):
        """Validate default filename pattern."""
        if not v:
            raise ValueError('Default filename cannot be empty')
        return v
    
    class Config:
        """Pydantic configuration."""
        extra = "forbid"
        validate_assignment = True


class BlockDefaultValues(BaseModel):
    """Schema for block default values."""
    id: int = Field(default=-1, description="Block ID")
    version: str = Field(default="0.0.1", description="Block version")
    x: int = Field(default=0, ge=0, description="X position")
    y: int = Field(default=0, ge=0, description="Y position")
    is_collapsed: bool = Field(default=False, description="Collapsed state")
    type: str = Field(default="", description="Block type")
    language: str = Field(default="", description="Programming language")
    extension: str = Field(default="", description="File extension")
    file: Optional[str] = Field(default=None, description="Block file")
    help: str = Field(default="", description="Help text")
    label: str = Field(default="A", description="Block label")
    color: str = Field(default="#000000", description="Block color")
    group: str = Field(default="Undefined", description="Block group")
    ports: List[Dict[str, Any]] = Field(default_factory=list, description="Block ports")
    maxIO: int = Field(default=0, ge=0, description="Maximum I/O")
    properties: List[Dict[str, Any]] = Field(default_factory=list, description="Block properties")
    codes: Dict[str, Any] = Field(default_factory=dict, description="Block codes")
    gen_codes: Dict[str, Any] = Field(default_factory=dict, description="Generated codes")
    weight: int = Field(default=0, description="Block weight")
    connections: List[Dict[str, Any]] = Field(default_factory=list, description="Block connections")
    
    @validator('color')
    def validate_color(cls, v):
        """Validate color format."""
        if not v.startswith('#') or len(v) != 7:
            raise ValueError('Color must be in hex format (#RRGGBB)')
        return v
    
    @validator('label')
    def validate_label(cls, v):
        """Validate label is not empty."""
        if not v.strip():
            raise ValueError('Label cannot be empty')
        return v
    
    class Config:
        """Pydantic configuration."""
        extra = "forbid"
        validate_assignment = True


class ColorFormats(BaseModel):
    """Schema for color formats configuration."""
    hex: str = Field(default="#RRGGBB", description="Hex color format")
    rgba: str = Field(default="R:G:B:A", description="RGBA color format")
    default: str = Field(default="#000000", description="Default color")
    
    class Config:
        """Pydantic configuration."""
        extra = "forbid"
        validate_assignment = True


class BlockDefaults(BaseModel):
    """Schema for block defaults configuration."""
    default_values: BlockDefaultValues = Field(default_factory=BlockDefaultValues, description="Default values for blocks")
    color_formats: ColorFormats = Field(default_factory=ColorFormats, description="Color format configuration")
    groups: List[str] = Field(default_factory=lambda: ["Undefined", "Input", "Output", "Processing", "GUI", "Math", "Logic", "Control"], description="Available block groups")
    
    class Config:
        """Pydantic configuration."""
        extra = "forbid"
        validate_assignment = True


class PortDefaultValues(BaseModel):
    """Schema for port default values."""
    version: str = Field(default="0.0.1", description="Port version")
    type: str = Field(default="", description="Port type")
    language: str = Field(default="", description="Programming language")
    hint: str = Field(default="", description="Port hint")
    color: str = Field(default="#000", description="Port color")
    multiple: bool = Field(default=False, description="Multiple connections allowed")
    code: str = Field(default="", description="Port code")
    var_name: str = Field(default="$block[label]$_$block[id]$_$port[name]$", description="Variable name pattern")
    conn_type: Optional[str] = Field(default=None, description="Connection type")
    name: Optional[str] = Field(default=None, description="Port name")
    label: Optional[str] = Field(default=None, description="Port label")
    index: int = Field(default=-1, ge=-1, description="Port index")
    type_index: int = Field(default=-1, ge=-1, description="Port type index")
    file: Optional[str] = Field(default=None, description="Port file")
    
    @validator('color')
    def validate_color(cls, v):
        """Validate color format."""
        if not v.startswith('#') or len(v) not in [4, 7]:
            raise ValueError('Color must be in hex format (#RGB or #RRGGBB)')
        return v
    
    @validator('conn_type')
    def validate_conn_type(cls, v):
        """Validate connection type."""
        if v is not None and v not in ['INPUT', 'OUTPUT']:
            raise ValueError('Connection type must be INPUT or OUTPUT')
        return v
    
    class Config:
        """Pydantic configuration."""
        extra = "forbid"
        validate_assignment = True


class ConnectionTypes(BaseModel):
    """Schema for connection types configuration."""
    input: str = Field(default="input", description="Input connection type")
    output: str = Field(default="output", description="Output connection type")
    
    class Config:
        """Pydantic configuration."""
        extra = "forbid"
        validate_assignment = True


class PortColorFormats(BaseModel):
    """Schema for port color formats configuration."""
    default: str = Field(default="#000", description="Default port color")
    input: str = Field(default="#0000FF", description="Input port color")
    output: str = Field(default="#FF0000", description="Output port color")
    
    class Config:
        """Pydantic configuration."""
        extra = "forbid"
        validate_assignment = True


class VariablePatterns(BaseModel):
    """Schema for variable patterns configuration."""
    default: str = Field(default="$block[label]$_$block[id]$_$port[name]$", description="Default variable pattern")
    simple: str = Field(default="$block[id]$_$port[name]$", description="Simple variable pattern")
    named: str = Field(default="$block[label]$_$port[name]$", description="Named variable pattern")
    
    class Config:
        """Pydantic configuration."""
        extra = "forbid"
        validate_assignment = True


class PortDefaults(BaseModel):
    """Schema for port defaults configuration."""
    default_values: PortDefaultValues = Field(default_factory=PortDefaultValues, description="Default values for ports")
    connection_types: ConnectionTypes = Field(default_factory=ConnectionTypes, description="Connection types configuration")
    color_formats: PortColorFormats = Field(default_factory=PortColorFormats, description="Port color formats")
    variable_patterns: VariablePatterns = Field(default_factory=VariablePatterns, description="Variable patterns configuration")
    
    class Config:
        """Pydantic configuration."""
        extra = "forbid"
        validate_assignment = True


class ValidationResult(BaseModel):
    """Schema for validation results."""
    success: bool = Field(description="Validation success status")
    errors: List[str] = Field(default_factory=list, description="Validation errors")
    warnings: List[str] = Field(default_factory=list, description="Validation warnings")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Validated data")
    
    class Config:
        """Pydantic configuration."""
        extra = "forbid"
        validate_assignment = True


class PydanticValidator:
    """
    Advanced validator using Pydantic for configuration validation.
    """
    
    @staticmethod
    def validate_system_config(data: Dict[str, Any]) -> ValidationResult:
        """
        Validate system configuration using Pydantic.
        
        Args:
            data: System configuration data
            
        Returns:
            ValidationResult with validation status
        """
        try:
            validated_data = SystemConfig(**data)
            return ValidationResult(
                success=True,
                data=validated_data.dict(),
                warnings=[]
            )
        except Exception as e:
            return ValidationResult(
                success=False,
                errors=[str(e)],
                warnings=[]
            )
    
    @staticmethod
    def validate_preferences(data: Dict[str, Any]) -> ValidationResult:
        """
        Validate preferences configuration using Pydantic.
        
        Args:
            data: Preferences configuration data
            
        Returns:
            ValidationResult with validation status
        """
        try:
            validated_data = Preferences(**data)
            return ValidationResult(
                success=True,
                data=validated_data.dict(),
                warnings=[]
            )
        except Exception as e:
            return ValidationResult(
                success=False,
                errors=[str(e)],
                warnings=[]
            )
    
    @staticmethod
    def validate_block_defaults(data: Dict[str, Any]) -> ValidationResult:
        """
        Validate block defaults configuration using Pydantic.
        
        Args:
            data: Block defaults configuration data
            
        Returns:
            ValidationResult with validation status
        """
        try:
            validated_data = BlockDefaults(**data)
            return ValidationResult(
                success=True,
                data=validated_data.dict(),
                warnings=[]
            )
        except Exception as e:
            return ValidationResult(
                success=False,
                errors=[str(e)],
                warnings=[]
            )
    
    @staticmethod
    def validate_port_defaults(data: Dict[str, Any]) -> ValidationResult:
        """
        Validate port defaults configuration using Pydantic.
        
        Args:
            data: Port defaults configuration data
            
        Returns:
            ValidationResult with validation status
        """
        try:
            validated_data = PortDefaults(**data)
            return ValidationResult(
                success=True,
                data=validated_data.dict(),
                warnings=[]
            )
        except Exception as e:
            return ValidationResult(
                success=False,
                errors=[str(e)],
                warnings=[]
            )
    
    @staticmethod
    def validate_all_configs() -> Dict[str, ValidationResult]:
        """
        Validate all configuration files using Pydantic.
        
        Returns:
            Dictionary mapping config names to validation results
        """
        from mosaicode.utils.config_loader import ConfigLoader
        
        results = {}
        
        # Validate system config
        try:
            system_data = ConfigLoader.load_config("system", validate=False)
            if system_data:
                results["system"] = PydanticValidator.validate_system_config(system_data)
            else:
                results["system"] = ValidationResult(
                    success=False,
                    errors=["System config not found or empty"]
                )
        except Exception as e:
            results["system"] = ValidationResult(
                success=False,
                errors=[f"Error loading system config: {e}"]
            )
        
        # Validate preferences
        try:
            preferences_data = ConfigLoader.load_config("preferences", validate=False)
            if preferences_data:
                results["preferences"] = PydanticValidator.validate_preferences(preferences_data)
            else:
                results["preferences"] = ValidationResult(
                    success=False,
                    errors=["Preferences config not found or empty"]
                )
        except Exception as e:
            results["preferences"] = ValidationResult(
                success=False,
                errors=[f"Error loading preferences: {e}"]
            )
        
        # Validate block defaults
        try:
            block_defaults_data = ConfigLoader.load_template("defaults", "blocks", validate=False)
            if block_defaults_data:
                results["block_defaults"] = PydanticValidator.validate_block_defaults(block_defaults_data)
            else:
                results["block_defaults"] = ValidationResult(
                    success=False,
                    errors=["Block defaults config not found or empty"]
                )
        except Exception as e:
            results["block_defaults"] = ValidationResult(
                success=False,
                errors=[f"Error loading block defaults: {e}"]
            )
        
        # Validate port defaults
        try:
            port_defaults_data = ConfigLoader.load_template("defaults", "ports", validate=False)
            if port_defaults_data:
                results["port_defaults"] = PydanticValidator.validate_port_defaults(port_defaults_data)
            else:
                results["port_defaults"] = ValidationResult(
                    success=False,
                    errors=["Port defaults config not found or empty"]
                )
        except Exception as e:
            results["port_defaults"] = ValidationResult(
                success=False,
                errors=[f"Error loading port defaults: {e}"]
            )
        
        return results 
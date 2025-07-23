# -*- coding: utf-8 -*-
"""
This module contains the System class.
"""
import datetime
import inspect  # For module inspect
import logging
import os
import pkgutil  # For dynamic package load
import sys
import time
from copy import copy
from functools import lru_cache, cached_property
from pathlib import Path
from typing import Dict, List, Optional, Any
import glob

from mosaicode.control.blockcontrol import BlockControl
from mosaicode.control.codetemplatecontrol import CodeTemplateControl
from mosaicode.control.portcontrol import PortControl
from mosaicode.model.blockmodel import BlockModel
from mosaicode.model.codetemplate import CodeTemplate
from mosaicode.model.port import Port
from mosaicode.model.preferences import Preferences
from mosaicode.persistence.preferencespersistence import PreferencesPersistence
from mosaicode.exceptions import ConfigurationError, FileOperationError
from mosaicode.utils.logger import get_logger

# Configure logging
logger = get_logger(__name__)


class System:
    """
    This class contains methods related the System class with performance optimizations.
    """

    APP = 'mosaicode'
    ZOOM_ORIGINAL = 1
    ZOOM_IN = 2
    ZOOM_OUT = 3

    VERSION = "0.0.1"
    DATA_DIR = str(Path.home() / "mosaicode")
    
    # Instance variable to the singleton
    instance: Optional['System.__Singleton'] = None

    @classmethod
    @lru_cache(maxsize=1)
    def load_system_config(cls) -> Dict[str, Any]:
        """
        Load system configuration from JSON with caching.
        
        Returns:
            Dictionary containing system configuration
            
        Raises:
            ConfigurationError: If system configuration is invalid
        """
        from mosaicode.utils.config_loader import ConfigLoader
        try:
            return ConfigLoader.load_config("system")
        except (ConfigurationError, FileOperationError) as e:
            logger.warning(f"Failed to load system config: {e}")
            return {}
    
    @classmethod
    @lru_cache(maxsize=32)
    def get_system_value(cls, key: str, default: Any = None) -> Any:
        """
        Get a system configuration value with caching.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        config = cls.load_system_config()
        return config.get(key, default)
    
    @classmethod
    @lru_cache(maxsize=1)
    def get_user_dir(cls) -> Path:
        """
        Get user directory path with caching.
        
        Returns:
            Path to user directory
        """
        return Path.home() / cls.APP
    
    @classmethod
    def log(cls, msg: str) -> None:
        """
        Log a message using the structured logger.
        
        Args:
            msg: Message to log
        """
        logger.error(f"System: {msg}")

    # ----------------------------------------------------------------------
    # An inner class instance to be singleton
    # ----------------------------------------------------------------------
    class __Singleton:
        # ----------------------------------------------------------------------

        def __init__(self):
            self.Log = None
            self.__code_templates: Dict[str, CodeTemplate] = {}
            self.__blocks: Dict[str, BlockModel] = {}
            self.__ports: Dict[str, Port] = {}

            self.list_of_examples: List[str] = []
            
            # Lazy loading flags
            self._blocks_loaded = False
            self._ports_loaded = False
            self._templates_loaded = False
            self._examples_loaded = False
            
            # Create user directory if does not exist
            directories = ["extensions",
                           "images",
                           "code-gen"]
            user_dir = System.get_user_dir()
            for name in directories:
                path = user_dir / name
                if not path.is_dir():
                    try:
                        path.mkdir(parents=True, exist_ok=True)
                        logger.info(f"Created directory: {path}")
                    except Exception as error:
                        error_msg = f"Error creating directory {path}: {error}"
                        logger.error(error_msg)
                        System.log(error_msg)

            try:
                self.__preferences = PreferencesPersistence.load(user_dir)
                logger.info("Preferences loaded successfully")
                logger.debug(f"[DEBUG] __init__ - preferences loaded from user_dir: '{user_dir}'")
                logger.debug(f"[DEBUG] __init__ - default_directory loaded: '{self.__preferences.default_directory}'")
            except Exception as e:
                logger.error(f"Failed to load preferences: {e}")
                self.__preferences = Preferences()
                logger.debug(f"[DEBUG] __init__ - using default preferences, default_directory: '{self.__preferences.default_directory}'")

        # ----------------------------------------------------------------------
        def reload(self) -> None:
            """Reload extensions and examples."""
            logger.info("Reloading system components")
            # Reset lazy loading flags
            self._blocks_loaded = False
            self._ports_loaded = False
            self._templates_loaded = False
            self._examples_loaded = False
            # Clear caches
            self.__blocks.clear()
            self.__ports.clear()
            self.__code_templates.clear()
            self.list_of_examples.clear()
            # Reload
            self.__load_examples()
            self.__load_extensions()

        # ----------------------------------------------------------------------
        def get_blocks(self) -> Dict[str, BlockModel]:
            """Get blocks with lazy loading."""
            if not self._blocks_loaded:
                self.__load_extensions()
            return copy(self.__blocks)

        # ----------------------------------------------------------------------
        def remove_block(self, block) -> Optional[BlockModel]:
            try:
                return self.__blocks.pop(block.type)
            except KeyError:
                logger.warning(f"Block not found for removal: {block.type}")
                return None

        # ----------------------------------------------------------------------
        def get_code_templates(self) -> Dict[str, CodeTemplate]:
            """Get code templates with lazy loading."""
            if not self._templates_loaded:
                self.__load_extensions()
            return copy(self.__code_templates)

        # ----------------------------------------------------------------------
        def get_ports(self) -> Dict[str, Port]:
            """Get ports with lazy loading."""
            if not self._ports_loaded:
                self.__load_extensions()
            return copy(self.__ports)

        # ----------------------------------------------------------------------
        def get_preferences(self) -> Preferences:
            return self.__preferences

        # ----------------------------------------------------------------------
        def __load_examples(self) -> None:
            """Load example files with caching."""
            if self._examples_loaded:
                return
            logger.debug("Loading examples")
            self.list_of_examples.clear()
            extension_path = os.path.join(System.get_user_dir(),"extensions")
            for language in os.listdir(extension_path):
                path = os.path.join(extension_path, language)
                path = os.path.join(path, "examples")
                for filename in os.listdir(path):
                    file_path = os.path.join(path, filename)
                    if filename.endswith(".mscd"):
                        self.list_of_examples.append(file_path)
            self.list_of_examples.sort()
            logger.info(f"Exemplos encontrados: {len(self.list_of_examples)}")
            self._examples_loaded = True

        # ----------------------------------------------------------------------
        def __load_extensions(self) -> None:
            """Carrega blocos, portas e templates a partir de arquivos JSON com lazy loading."""
            logger.info("Carregando extensões do diretório extensions do usuário e do projeto")
            from mosaicode.persistence.blockpersistence import BlockPersistence
            from mosaicode.persistence.portpersistence import PortPersistence
            from mosaicode.persistence.codetemplatepersistence import CodeTemplatePersistence
            from mosaicode.model.blockmodel import BlockModel
            from mosaicode.model.port import Port
            from mosaicode.model.codetemplate import CodeTemplate
            import os

            # Only clear if not already loaded
            if not self._blocks_loaded:
                self.__blocks.clear()
            if not self._ports_loaded:
                self.__ports.clear()
            if not self._templates_loaded:
                self.__code_templates.clear()

            user_dir = System.get_user_dir() / "extensions"
            search_paths = []
            if user_dir.exists():
                search_paths.append(str(user_dir))

            # Adiciona todas as pastas mosaicode-*/**/extensions do projeto
            project_root = Path(os.getcwd())
            for ext_dir in project_root.glob("mosaicode-*/mosaicode_lib_*/extensions"):
                if ext_dir.is_dir():
                    search_paths.append(str(ext_dir))

            # Carregar portas (lazy loading)
            if not self._ports_loaded:
                for base_path in search_paths:
                    for root, dirs, files in os.walk(base_path):
                        if Path(root).name == "ports":
                            for file in files:
                                if file.endswith(".json"):
                                    file_path = str(Path(root) / file)
                                    port = PortPersistence.load(file_path)
                                    if port and hasattr(port, 'type'):
                                        self.__ports[port.type] = port
                                        logger.info(f"Porta carregada: {port.type} de {file_path}")
                self._ports_loaded = True

            # Carregar blocos (lazy loading) - Priorizar arquivos JSON sobre Python
            if not self._blocks_loaded:
                # Primeiro, carregar blocos de arquivos JSON
                json_blocks = {}
                for base_path in search_paths:
                    logger.debug(f"[DEBUG] Procurando blocos JSON em: {base_path}")
                    for root, dirs, files in os.walk(base_path):
                        if Path(root).name == "blocks":
                            # Pular a pasta backup_jsons
                            if "backup_jsons" in dirs:
                                dirs.remove("backup_jsons")
                                logger.debug(f"[DEBUG] Pulando pasta backup_jsons em: {root}")
                            
                            logger.debug(f"[DEBUG] Encontrada pasta de blocos: {root}")
                            for dirpath, dirnames, filenames in os.walk(root):
                                # Pular backup_jsons recursivamente
                                if "backup_jsons" in dirpath:
                                    continue
                                    
                                for file in filenames:
                                    if file.endswith(".json"):
                                        file_path = str(Path(dirpath) / file)
                                        logger.debug(f"[DEBUG] Tentando carregar bloco JSON: {file_path}")
                                        try:
                                            block = BlockPersistence.load(file_path)
                                            if block and hasattr(block, 'type'):
                                                json_blocks[block.type] = block
                                                logger.info(f"Bloco JSON carregado: {block.type} de {file_path}")
                                            else:
                                                logger.warning(f"Bloco JSON inválido ou sem tipo: {file_path}")
                                        except Exception as e:
                                            logger.error(f"Erro ao carregar bloco JSON {file_path}: {e}")
                
                # Depois, carregar blocos de arquivos Python apenas se não existir JSON equivalente
                for base_path in search_paths:
                    logger.debug(f"[DEBUG] Procurando blocos Python em: {base_path}")
                    for root, dirs, files in os.walk(base_path):
                        if Path(root).name == "blocks":
                            # Pular a pasta backup_jsons
                            if "backup_jsons" in dirs:
                                dirs.remove("backup_jsons")
                                logger.debug(f"[DEBUG] Pulando pasta backup_jsons em: {root}")
                            
                            for file in files:
                                if file.endswith(".py") and file != "__init__.py":
                                    file_path = str(Path(root) / file)
                                    logger.debug(f"[DEBUG] Tentando carregar bloco Python: {file_path}")
                                    try:
                                        # Importa o módulo
                                        module_name = str(Path(file_path).relative_to(Path(__file__).parent.parent)).replace("/", ".").replace(".py", "")
                                        if module_name.startswith("extensions."):
                                            module_name = module_name[11:]  # Remove "extensions."
                                        
                                        # Adiciona o diretório ao sys.path se necessário
                                        if str(Path(root).parent) not in sys.path:
                                            sys.path.insert(0, str(Path(root).parent))
                                        
                                        # Importa o módulo
                                        module = __import__(module_name, fromlist=["*"])
                                        
                                        # Procura por classes que herdam de BlockModel
                                        for name, obj in inspect.getmembers(module):
                                            if (inspect.isclass(obj) and 
                                                hasattr(obj, '__bases__') and 
                                                any('BlockModel' in str(base) for base in obj.__bases__) and
                                                obj.__name__ != 'BlockModel'):
                                                try:
                                                    instance = obj()
                                                    if hasattr(instance, 'type') and instance.type:
                                                        # Só adiciona se não existir um JSON equivalente
                                                        if instance.type not in json_blocks:
                                                            self.__blocks[instance.type] = instance
                                                            logger.info(f"Bloco Python carregado: {instance.type} de {file_path}")
                                                        else:
                                                            logger.info(f"Bloco Python ignorado (existe JSON): {instance.type} de {file_path}")
                                                    else:
                                                        # Para blocos sem tipo, usar o nome da classe
                                                        if obj.__name__ not in json_blocks:
                                                            self.__blocks[obj.__name__] = instance
                                                            logger.info(f"Bloco Python carregado: {obj.__name__} de {file_path}")
                                                        else:
                                                            logger.info(f"Bloco Python ignorado (existe JSON): {obj.__name__} de {file_path}")
                                                except Exception as e:
                                                    logger.error(f"Erro ao instanciar bloco Python {obj.__name__}: {e}")
                                    except Exception as e:
                                        logger.error(f"Erro ao carregar bloco Python {file_path}: {e}")
                
                # Adicionar todos os blocos JSON ao dicionário final
                self.__blocks.update(json_blocks)
                self._blocks_loaded = True

            # Carregar code templates (lazy loading)
            if not self._templates_loaded:
                for base_path in search_paths:
                    for root, dirs, files in os.walk(base_path):
                        if Path(root).name == "codetemplates":
                            for file in files:
                                if file.endswith(".json"):
                                    file_path = str(Path(root) / file)
                                    template = CodeTemplatePersistence.load(file_path)
                                    if template and hasattr(template, 'type'):
                                        self.__code_templates[template.type] = template
                                        logger.info(f"Code template carregado: {template.type} de {file_path}")
                self._templates_loaded = True

            logger.info(f"Total de blocos carregados: {len(self.__blocks)}")
            logger.info(f"Total de portas carregadas: {len(self.__ports)}")
            logger.info(f"Total de code templates carregados: {len(self.__code_templates)}")

    # ----------------------------------------------------------------------
    def __init__(self):
        """Initialize System singleton."""
        if System.instance is None:
            System.instance = System.__Singleton()
            logger.info("System initialized")

    # ----------------------------------------------------------------------
    @classmethod
    def get_blocks(cls) -> Dict[str, BlockModel]:
        """Get all loaded blocks."""
        if cls.instance is None:
            cls.instance = cls.__Singleton()
        return cls.instance.get_blocks()

    # ----------------------------------------------------------------------
    @classmethod
    def get_code_templates(cls) -> Dict[str, CodeTemplate]:
        """Get all loaded code templates."""
        if cls.instance is None:
            cls.instance = cls.__Singleton()
        return cls.instance.get_code_templates()

    # ----------------------------------------------------------------------
    @classmethod
    def get_ports(cls) -> Dict[str, Port]:
        """Get all loaded ports."""
        if cls.instance is None:
            cls.instance = cls.__Singleton()
        return cls.instance.get_ports()

    # ----------------------------------------------------------------------
    @classmethod
    def get_preferences(cls) -> Preferences:
        """
        Get system preferences.
        
        Returns:
            Preferences instance
        """
        if cls.instance is None:
            cls.instance = cls.__Singleton()
        
        preferences = cls.instance.get_preferences()
#        logger.debug(f"[DEBUG] get_preferences - returning preferences with default_directory: '{preferences.default_directory}'")
        return preferences

    # ----------------------------------------------------------------------
    @classmethod
    def reload(cls) -> None:
        """Reload system components."""
        if cls.instance is None:
            cls.instance = cls.__Singleton()
        cls.instance.reload()

    # ----------------------------------------------------------------------
    @classmethod
    def set_log(cls, log_widget) -> None:
        """Set log widget for GUI logging."""
        if cls.instance is None:
            cls.instance = cls.__Singleton()
        cls.instance.Log = log_widget
        logger.info("Log widget set")

    # ----------------------------------------------------------------------
    @classmethod
    def remove_block(cls, block) -> Optional[BlockModel]:
        """Remove a block from the system."""
        if cls.instance is None:
            cls.instance = cls.__Singleton()
        return cls.instance.remove_block(block)

    # ----------------------------------------------------------------------
    @classmethod
    def get_list_of_examples(cls) -> List[str]:
        """Get list of example files."""
        if cls.instance is None:
            cls.instance = cls.__Singleton()
        return cls.instance.list_of_examples

    # ----------------------------------------------------------------------
    @classmethod
    def get_examples(cls) -> List[str]:
        """Get list of example files (alias for get_list_of_examples)."""
        return cls.get_list_of_examples()

    # ----------------------------------------------------------------------
    @classmethod
    def replace_wildcards(cls, name: str, diagram) -> str:
        """
        This method replace the wildcards.

        Returns:

            * **Types** (:class:`str<str>`)
        """
        result = name.replace("%t", str(time.time()))
        date = datetime.datetime.now().strftime("(%Y-%m-%d-%H:%M:%S)")
        result = result.replace("%d", date)
        result = result.replace("%l", diagram.language)
        result = result.replace("%n", diagram.patch_name)
        result = result.replace(" ", "_")
        return result

    # ----------------------------------------------------------------------
    @classmethod
    def get_dir_name(cls, diagram) -> str:
        """
        This method return the directory name.

        Returns:

            * **Types** (:class:`str<str>`)
        """
        name = System.get_preferences().default_directory
        logger.debug(f"[DEBUG] get_dir_name - default_directory from preferences: '{name}'")
        
        name = System.replace_wildcards(name, diagram)
        logger.debug(f"[DEBUG] get_dir_name - after replace_wildcards: '{name}'")
        
        # NOVO: Se não for absoluto, resolva relativo à home antiga
        if not Path(name).is_absolute():
            old_path = str(System.get_user_dir() / name)
            logger.debug(f"[DEBUG] get_dir_name - path not absolute, resolving to: '{old_path}'")
            name = old_path
        else:
            logger.debug(f"[DEBUG] get_dir_name - path is absolute: '{name}'")
            
        if not name.endswith("/"):
            name = name + "/"
        
        logger.debug(f"[DEBUG] get_dir_name - final path: '{name}'")
        return name


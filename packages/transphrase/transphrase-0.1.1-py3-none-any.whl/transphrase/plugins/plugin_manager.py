import importlib
import inspect
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Type

import yaml


class PluginInterface:
    """Base interface for plugins"""

    @classmethod
    def get_name(cls) -> str:
        """Get the name of the plugin"""
        return cls.__name__

    @classmethod
    def get_description(cls) -> str:
        """Get the description of the plugin"""
        return cls.__doc__ or "No description provided"


class PromptTemplate(PluginInterface):
    """Base class for prompt template plugins"""

    @classmethod
    def get_system_prompt(cls) -> str:
        """Get the system prompt template"""
        raise NotImplementedError("Prompt templates must implement get_system_prompt")

    @classmethod
    def format_prompt(cls, **kwargs) -> str:
        """Format the prompt with the given parameters"""
        return cls.get_system_prompt().format(**kwargs)


class ProcessorModule(PluginInterface):
    """Base class for text processor modules"""

    def process_text(self, text: str) -> str:
        """Process the input text"""
        raise NotImplementedError("Processor modules must implement process_text")


class PluginManager:
    """Manager for plugin discovery and loading"""

    def __init__(self, plugin_dirs: List[str] = None):
        """
        Initialize plugin manager

        Args:
            plugin_dirs: List of directories to search for plugins
        """
        self.plugin_dirs = plugin_dirs or [
            "~/.transphrase/plugins",
            os.path.join(os.path.dirname(__file__), "builtin"),
        ]
        self.plugin_dirs = [Path(p).expanduser() for p in self.plugin_dirs]

        self.prompt_templates: Dict[str, Type[PromptTemplate]] = {}
        self.processor_modules: Dict[str, Type[ProcessorModule]] = {}

        # Load plugins
        self.discover_plugins()

    def discover_plugins(self) -> None:
        """Discover and load plugins from plugin directories"""
        for plugin_dir in self.plugin_dirs:
            if not plugin_dir.exists():
                continue

            # Add plugin directory to Python path
            sys.path.insert(0, str(plugin_dir))

            # Scan for Python files
            for py_file in plugin_dir.glob("*.py"):
                if py_file.name.startswith("_"):
                    continue

                module_name = py_file.stem
                try:
                    module = importlib.import_module(module_name)

                    # Find plugin classes in the module
                    for _, obj in inspect.getmembers(module, inspect.isclass):
                        if issubclass(obj, PromptTemplate) and obj is not PromptTemplate:
                            self.prompt_templates[obj.get_name()] = obj
                        elif issubclass(obj, ProcessorModule) and obj is not ProcessorModule:
                            self.processor_modules[obj.get_name()] = obj

                except Exception as e:
                    print(f"Error loading plugin {module_name}: {e}")

            # Remove plugin directory from Python path
            sys.path.pop(0)

    def get_prompt_template(self, name: str) -> Optional[Type[PromptTemplate]]:
        """Get prompt template by name"""
        return self.prompt_templates.get(name)

    def get_processor_module(self, name: str) -> Optional[Type[ProcessorModule]]:
        """Get processor module by name"""
        return self.processor_modules.get(name)

    def list_prompt_templates(self) -> List[Dict[str, str]]:
        """List available prompt templates"""
        return [
            {"name": cls.get_name(), "description": cls.get_description()}
            for cls in self.prompt_templates.values()
        ]

    def list_processor_modules(self) -> List[Dict[str, str]]:
        """List available processor modules"""
        return [
            {"name": cls.get_name(), "description": cls.get_description()}
            for cls in self.processor_modules.values()
        ]

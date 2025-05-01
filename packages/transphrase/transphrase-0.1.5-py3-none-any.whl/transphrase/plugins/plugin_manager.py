import importlib
import inspect
import os
import sys
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional, Type

import yaml
from rich.console import Console

console = Console()


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
            "~/.transphrase/plugins/prompt_templates",
            "~/.transphrase/plugins/processors",
        ]
        self.plugin_dirs = [Path(p).expanduser() for p in self.plugin_dirs]

        self.prompt_templates: Dict[str, Type[PromptTemplate]] = {}
        self.processor_modules: Dict[str, Type[ProcessorModule]] = {}

        # Map of plugin name to file path for error reporting
        self.plugin_paths: Dict[str, str] = {}

        # Validation errors
        self.validation_errors: Dict[str, str] = {}

        # Load plugins
        self.discover_plugins()

    def validate_prompt_template(self, cls: Type[PromptTemplate]) -> Optional[str]:
        """Validate a prompt template class"""
        # Check if get_system_prompt is implemented
        try:
            prompt = cls.get_system_prompt()
            if not isinstance(prompt, str):
                return "get_system_prompt() must return a string"

            # Try to format with sample parameters to validate
            try:
                cls.format_prompt(source_language="English", target_language="Spanish")
            except KeyError as e:
                return f"Missing required format parameter: {e}"
            except Exception as e:
                return f"Error formatting prompt: {e}"

            return None
        except NotImplementedError:
            return "get_system_prompt() must be implemented"
        except Exception as e:
            return f"Error in get_system_prompt(): {e}"

    def validate_processor_module(self, cls: Type[ProcessorModule]) -> Optional[str]:
        """Validate a processor module class"""
        # Check if process_text is implemented
        try:
            # Try to create an instance
            instance = cls()

            # Check if process_text is implemented
            if not hasattr(instance, "process_text"):
                return "process_text() method missing"

            # Try with sample text to validate
            try:
                result = instance.process_text("Sample text")
                if not isinstance(result, str):
                    return "process_text() must return a string"
                return None
            except Exception as e:
                return f"Error in process_text(): {e}"
        except Exception as e:
            return f"Error instantiating processor: {e}"

    def discover_plugins(self) -> None:
        """Discover and load plugins from plugin directories"""
        console.print("[bold]Discovering plugins...[/bold]")

        for plugin_dir in self.plugin_dirs:
            if not plugin_dir.exists():
                console.print(f"[yellow]Plugin directory not found: {plugin_dir}[/yellow]")
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
                    for class_name, obj in inspect.getmembers(module, inspect.isclass):
                        plugin_name = obj.get_name()
                        plugin_path = str(py_file)

                        # Save plugin path for error reporting
                        self.plugin_paths[plugin_name] = plugin_path

                        # Check for prompt templates
                        if issubclass(obj, PromptTemplate) and obj is not PromptTemplate:
                            # Validate
                            error = self.validate_prompt_template(obj)
                            if error:
                                self.validation_errors[plugin_name] = error
                                console.print(
                                    f"[yellow]Warning: Prompt template '{plugin_name}' has error: {error}[/yellow]"
                                )
                            else:
                                self.prompt_templates[plugin_name] = obj
                                console.print(
                                    f"[green]Loaded prompt template: {plugin_name}[/green]"
                                )

                        # Check for processor modules
                        elif issubclass(obj, ProcessorModule) and obj is not ProcessorModule:
                            # Validate
                            error = self.validate_processor_module(obj)
                            if error:
                                self.validation_errors[plugin_name] = error
                                console.print(
                                    f"[yellow]Warning: Processor module '{plugin_name}' has error: {error}[/yellow]"
                                )
                            else:
                                self.processor_modules[plugin_name] = obj
                                console.print(
                                    f"[green]Loaded processor module: {plugin_name}[/green]"
                                )

                except Exception as e:
                    console.print(f"[red]Error loading plugin {module_name}: {e}[/red]")
                    console.print(f"[dim]{traceback.format_exc()}[/dim]")

            # Remove plugin directory from Python path
            sys.path.pop(0)

        # Summary
        if self.prompt_templates or self.processor_modules:
            console.print(
                f"[green]Loaded {len(self.prompt_templates)} prompt templates and {len(self.processor_modules)} processor modules[/green]"
            )
        else:
            console.print("[yellow]No plugins were loaded[/yellow]")

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

    def create_prompt_template(self, name: str, **kwargs: Any) -> Optional[str]:
        """Create a prompt template with the given name and parameters"""
        template_class = self.get_prompt_template(name)
        if not template_class:
            return None

        try:
            return template_class.format_prompt(**kwargs)
        except Exception as e:
            console.print(f"[red]Error creating prompt from template '{name}': {e}[/red]")
            return None

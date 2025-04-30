"""Plugin setup utilities for TransPhrase."""

import os
import shutil
from pathlib import Path
from typing import List

from rich.console import Console

console = Console()

PLUGIN_DIRS = [
    Path("~/.transphrase/plugins").expanduser(),
    Path("~/.transphrase/plugins/prompt_templates").expanduser(),
    Path("~/.transphrase/plugins/processors").expanduser(),
]

EXAMPLE_PROMPT_TEMPLATE = """
import yaml
from transphrase.plugins.plugin_manager import PromptTemplate

class NovelTranslationTemplate(PromptTemplate):
    \"\"\"Specialized template for translating novels with character and terminology tracking\"\"\"

    @classmethod
    def get_system_prompt(cls) -> str:
        return \"\"\"
You are a literary translator specializing in novels. Translate the following text from {source_language} to {target_language}.

Pay special attention to:
1. Character names and relationships
2. Setting and world-building terms
3. Maintain the author's tone and style
4. Preserve cultural nuances when possible

If you encounter any specialized terminology or recurring character names, maintain consistency throughout.

Format your translation using proper {target_language} conventions for:
- Dialogue
- Paragraphs
- Quotations
- Idiomatic expressions
\"\"\"
"""

EXAMPLE_PROCESSOR = """
from transphrase.plugins.plugin_manager import ProcessorModule

class NameConsistencyProcessor(ProcessorModule):
    \"\"\"Maintains consistency of character names across translations\"\"\"

    def __init__(self):
        self.name_map = {}

    def add_name_mapping(self, source_name: str, target_name: str) -> None:
        \"\"\"Add a name mapping to the processor\"\"\"
        self.name_map[source_name] = target_name

    def process_text(self, text: str) -> str:
        \"\"\"Process text to ensure name consistency\"\"\"
        result = text
        for source_name, target_name in self.name_map.items():
            result = result.replace(source_name, target_name)
        return result
"""

PLUGIN_README = """# TransPhrase Plugins

This directory contains plugins for the TransPhrase translation tool.

## Types of Plugins

TransPhrase supports two types of plugins:

### 1. Prompt Templates

Located in the `prompt_templates` directory, these plugins define custom system prompts for different translation scenarios.

To create a prompt template:
- Create a new Python file in the `prompt_templates` directory
- Define a class that inherits from `PromptTemplate`
- Implement the `get_system_prompt()` method

### 2. Text Processors

Located in the `processors` directory, these plugins can modify text before or after translation.

To create a text processor:
- Create a new Python file in the `processors` directory
- Define a class that inherits from `ProcessorModule`
- Implement the `process_text(text: str) -> str` method

## Example Usage

Check the included example plugins to understand how to create your own.
"""


def setup_plugin_directories() -> None:
    """Create plugin directories with example plugins if they don't exist."""
    # Create main plugin directories
    for plugin_dir in PLUGIN_DIRS:
        plugin_dir.mkdir(parents=True, exist_ok=True)

    # Create README file
    readme_path = PLUGIN_DIRS[0] / "README.md"
    if not readme_path.exists():
        with open(readme_path, "w") as f:
            f.write(PLUGIN_README)
        console.print(f"[green]Created plugin README at {readme_path}[/green]")

    # Create example prompt template
    prompt_template_path = PLUGIN_DIRS[1] / "novel_template.py"
    if not prompt_template_path.exists():
        with open(prompt_template_path, "w") as f:
            f.write(EXAMPLE_PROMPT_TEMPLATE)
        console.print(f"[green]Created example prompt template at {prompt_template_path}[/green]")

    # Create example processor
    processor_path = PLUGIN_DIRS[2] / "name_consistency.py"
    if not processor_path.exists():
        with open(processor_path, "w") as f:
            f.write(EXAMPLE_PROCESSOR)
        console.print(f"[green]Created example processor at {processor_path}[/green]")

    console.print("[bold green]Plugin directories and examples created successfully![/bold green]")
    console.print(f"[yellow]Plugin directory: {PLUGIN_DIRS[0]}[/yellow]")


def get_available_plugins() -> tuple[List[dict], List[dict]]:
    """Get available plugins from the plugin directories."""
    from transphrase.plugins.plugin_manager import PluginManager

    plugin_manager = PluginManager([str(dir_path) for dir_path in PLUGIN_DIRS])

    prompt_templates = plugin_manager.list_prompt_templates()
    processors = plugin_manager.list_processor_modules()

    return prompt_templates, processors

"""Configuration management for TransPhrase."""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from rich.console import Console
from rich.prompt import Confirm, Prompt

from transphrase.api.handler import APIHandler
from transphrase.core.config import (
    LANGUAGE_SPECIFIC_POLISH,
    POLISH_PROMPT_TEMPLATE,
    POLISH_STYLE_PRESETS,
    TRANSLATION_PROMPT_TEMPLATE,
    TranslationConfig,
)
from transphrase.ui.model_selector import ModelSelector

console = Console()

# Constants
SUPPORTED_LANGUAGES = ["Chinese", "English", "Japanese", "Korean", "Spanish", "French", "German"]
CONFIG_DIR = Path("~/.transphrase").expanduser()
CONFIG_FILE = CONFIG_DIR / "config.json"


def load_config_from_file() -> Optional[Dict[str, Any]]:
    """Load configuration from JSON file if it exists."""
    if not CONFIG_FILE.exists():
        return None

    try:
        with open(CONFIG_FILE, "r") as f:
            config_data = json.load(f)
        console.print(f"[green]Loaded configuration from {CONFIG_FILE}[/green]")
        return config_data
    except json.JSONDecodeError:
        console.print(
            f"[yellow]Warning: Config file exists but is not valid JSON. Using interactive mode.[/yellow]"
        )
        return None
    except Exception as e:
        console.print(
            f"[yellow]Warning: Failed to load config file: {e}. Using interactive mode.[/yellow]"
        )
        return None


def save_config_to_file(config: TranslationConfig) -> bool:
    """Save configuration to JSON file."""
    # Ensure config directory exists
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    # Convert config to serializable dictionary
    config_dict = {
        "api_key": config.api_key,
        "base_url": config.base_url,
        "model": config.model,
        # "mode": config.mode,
        "source_language": config.source_language,
        "target_language": config.target_language,
        # "source_dir": str(config.source_dir),
        # "output_dir": str(config.output_dir),
        "skip_existing": config.skip_existing,
        "workers": config.workers,
        "use_cache": config.use_cache,
        "cache_ttl": config.cache_ttl,
        "db_path": config.db_path,
        # Don't save system_prompt as it's generated from template
    }

    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config_dict, f, indent=2)
        console.print(f"[green]Configuration saved to {CONFIG_FILE}[/green]")
        return True
    except Exception as e:
        console.print(f"[yellow]Warning: Failed to save config file: {e}[/yellow]")
        return False


def get_api_credentials(config_data: Optional[Dict[str, Any]] = None) -> Tuple[str, str]:
    """Get API key and base URL from config, environment or prompt."""
    # Check config file first
    if config_data and "api_key" in config_data and config_data["api_key"]:
        api_key = config_data["api_key"]
        base_url = config_data.get("base_url", "https://api.electronhub.top")
        return api_key, base_url

    # Then check environment
    api_key = os.environ.get("MASTER_API_KEY", "")
    if not api_key:
        api_key = Prompt.ask("Enter your API key", password=True)
        if not api_key:
            console.print("[red]API key is required.[/red]")
            sys.exit(1)

    base_url = os.environ.get("API_BASE_URL", "https://api.electronhub.top")
    if config_data and "base_url" in config_data:
        base_url = config_data["base_url"]

    return api_key, base_url


def select_mode(config_data: Optional[Dict[str, Any]] = None) -> str:
    """Select operation mode (translate or polish) using arrow keys."""
    import readchar
    from rich.panel import Panel

    # Check config file first
    if config_data and "mode" in config_data and config_data["mode"]:
        selected_mode = config_data["mode"]
        if selected_mode in ["translate", "polish"]:
            console.print(f"[green]Using mode from config: {selected_mode}[/green]")
            return selected_mode

    # Available modes
    modes = ["translate", "polish"]
    mode_descriptions = {
        "translate": "Convert text from one language to another",
        "polish": "Improve an existing translation's fluency and readability",
    }

    # Default selection
    selected_index = 0

    # Function to render the mode selection screen
    def render_selection():
        console.clear()
        console.print("\n[bold]Operation Mode[/bold]")
        console.print("Use [blue]↑/↓[/blue] arrow keys to navigate, [blue]Enter[/blue] to select\n")

        for i, mode in enumerate(modes):
            if i == selected_index:
                # Highlight the selected mode
                console.print(
                    Panel(
                        f"[bold white]{mode}[/bold white]\n[blue]{mode_descriptions[mode]}[/blue]",
                        border_style="green",
                    )
                )
            else:
                console.print(
                    Panel(f"[white]{mode}[/white]\n{mode_descriptions[mode]}", border_style="blue")
                )

    # Interactive loop
    while True:
        render_selection()

        # Get keyboard input
        key = readchar.readkey()

        # Handle navigation keys
        if key == readchar.key.UP and selected_index > 0:
            selected_index -= 1
        elif key == readchar.key.DOWN and selected_index < len(modes) - 1:
            selected_index += 1
        elif key == readchar.key.ENTER:
            # Return the selected mode
            selected_mode = modes[selected_index]
            console.print(f"[green]Selected mode: {selected_mode}[/green]")
            return selected_mode
        # Allow 'q' or ESC to select the default (first) mode
        elif key == "q" or key == readchar.key.ESC:
            selected_mode = modes[0]
            console.print(f"[green]Selected default mode: {selected_mode}[/green]")
            return selected_mode


def select_model(api_handler: APIHandler, config_data: Optional[Dict[str, Any]] = None) -> str:
    """Select model for translation."""
    # Check config file first
    if config_data and "model" in config_data and config_data["model"]:
        selected_model = config_data["model"]
        console.print(f"[green]Using model from config: {selected_model}[/green]")
        return selected_model

    console.print("[bold]Select a model for processing:[/bold]")
    model_selector = ModelSelector(api_handler)
    selected_model = model_selector.select_model()
    console.print(f"[green]Selected model: {selected_model}[/green]")
    return selected_model


def select_languages(
    config_data: Optional[Dict[str, Any]] = None, auto_detect: bool = False
) -> Tuple[str, str]:
    """Select source and target languages for processing."""
    # Check config file first
    if config_data and "source_language" in config_data and "target_language" in config_data:
        source = config_data["source_language"]
        target = config_data["target_language"]
        if source in SUPPORTED_LANGUAGES and target in SUPPORTED_LANGUAGES and source != target:
            console.print(f"[green]Using languages from config: {source} → {target}[/green]")
            return source, target

    # If auto-detection is enabled, don't prompt for source language
    if auto_detect:
        console.print("[yellow]Source language will be auto-detected from files[/yellow]")
        source_language = ""  # Empty string indicates auto-detection should be used
    else:
        console.print("\n[bold]Language Selection:[/bold]")
        source_language = Prompt.ask(
            "Select source language", choices=SUPPORTED_LANGUAGES, default="Chinese"
        )

    # For target language, we always need to prompt
    # Filter out source language from target options if it's specified
    if source_language:
        target_choices = [lang for lang in SUPPORTED_LANGUAGES if lang != source_language]
    else:
        target_choices = SUPPORTED_LANGUAGES

    default_target = "English" if "English" in target_choices else target_choices[0]

    target_language = Prompt.ask(
        "Select target language", choices=target_choices, default=default_target
    )

    return source_language, target_language


def select_polish_style(config_data: Optional[Dict[str, Any]] = None) -> str:
    """Select polishing style when in polish mode."""
    import readchar
    from rich.panel import Panel

    # Check config file first
    if config_data and "polish_style" in config_data and config_data["polish_style"]:
        selected_style = config_data["polish_style"]
        if selected_style in ["standard", "formal", "creative", "technical", "conversational"]:
            console.print(f"[green]Using polish style from config: {selected_style}[/green]")
            return selected_style

    # Available styles with descriptions
    styles = {
        "standard": "Balanced, natural writing appropriate to context",
        "formal": "Elevated language with complex structures and precise terminology",
        "creative": "Rich imagery and expressive language with artistic flourishes",
        "technical": "Clear, precise language optimized for information density",
        "conversational": "Natural flow with casual markers and engaging tone",
    }

    # Get list of styles for indexed access
    style_names = list(styles.keys())
    style_descriptions = list(styles.values())

    # Default selection
    selected_index = 0

    # Function to render the style selection screen
    def render_selection():
        console.clear()
        console.print("\n[bold]Polish Style Selection[/bold]")
        console.print("Use [blue]↑/↓[/blue] arrow keys to navigate, [blue]Enter[/blue] to select\n")

        for i, (name, desc) in enumerate(zip(style_names, style_descriptions)):
            if i == selected_index:
                # Highlight the selected style
                console.print(
                    Panel(
                        f"[bold white]{name}[/bold white]\n[blue]{desc}[/blue]",
                        border_style="green",
                    )
                )
            else:
                console.print(Panel(f"[white]{name}[/white]\n{desc}", border_style="blue"))

    # Interactive loop
    while True:
        render_selection()

        # Get keyboard input
        key = readchar.readkey()

        # Handle navigation keys
        if key == readchar.key.UP and selected_index > 0:
            selected_index -= 1
        elif key == readchar.key.DOWN and selected_index < len(style_names) - 1:
            selected_index += 1
        elif key == readchar.key.ENTER:
            # Return the selected style
            selected_style = style_names[selected_index]
            console.print(f"[green]Selected polish style: {selected_style}[/green]")
            return selected_style
        # Allow 'q' or ESC to select the default (standard) style
        elif key == "q" or key == readchar.key.ESC:
            selected_style = "standard"
            console.print(f"[green]Selected default style: {selected_style}[/green]")
            return selected_style


def configure_paths(
    config_data: Optional[Dict[str, Any]] = None, mode: str = "translate"
) -> Tuple[Path, Path]:
    """Configure input and output paths with improved output directory selection.

    Args:
        config_data: Optional configuration data
        mode: The operation mode (translate or polish)

    Returns:
        Tuple of source and output paths
    """
    # Check config file first
    if config_data and "source_dir" in config_data and "output_dir" in config_data:
        source_path = Path(config_data["source_dir"]).expanduser().resolve()
        output_path = Path(config_data["output_dir"]).expanduser().resolve()

        # Validate paths
        if source_path.exists():
            # Create output directory if needed
            output_path.mkdir(parents=True, exist_ok=True)
            console.print(f"[green]Using paths from config: {source_path} → {output_path}[/green]")
            return source_path, output_path
        else:
            console.print(f"[yellow]Source path in config does not exist: {source_path}[/yellow]")

    console.print("\n[bold]File Selection:[/bold]")

    # Get source directory or file
    source_path_str = Prompt.ask("Enter source path (file or directory)")
    source_path = Path(source_path_str).expanduser().resolve()

    if not source_path.exists():
        console.print(f"[red]Source path '{source_path}' does not exist.[/red]")
        sys.exit(1)

    # Generate output directory options based on source path and mode
    output_options = generate_output_options(source_path, mode)

    # Let user select output directory with arrow keys
    output_path = select_output_directory(output_options, source_path)

    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)

    return source_path, output_path


def generate_output_options(source_path: Path, mode: str) -> Dict[str, Path]:
    """Generate smart output directory options based on source path and operation mode.

    Args:
        source_path: The source file or directory path
        mode: The operation mode (translate or polish)

    Returns:
        Dictionary of output options with description as key and path as value
    """
    # Mode-specific suffix
    suffix = "translated" if mode == "translate" else "polished"

    # Determine if source is file or directory
    is_file = source_path.is_file()

    options = {}

    if is_file:
        # File-specific options
        parent_dir = source_path.parent
        filename = source_path.stem

        # Option 1: Same directory with mode suffix
        options[f"Same directory with '{suffix}' suffix"] = (
            parent_dir / f"{filename}_{suffix}{source_path.suffix}"
        )

        # Option 2: Mode-specific subdirectory with same filename
        options[f"Subdirectory '{suffix}'"] = parent_dir / suffix / source_path.name

        # Option 3: Parent directory's parent with mode suffix directory
        if parent_dir.parent != parent_dir:  # Not root
            options["Output to parent's directory"] = parent_dir.parent / suffix / source_path.name
    else:
        # Directory-specific options
        parent_dir = source_path.parent
        dirname = source_path.name

        # Option 1: Sibling directory with mode suffix
        options[f"Sibling directory '{dirname}_{suffix}'"] = parent_dir / f"{dirname}_{suffix}"

        # Option 2: Subdirectory with mode name
        options[f"Subdirectory '{suffix}'"] = source_path / suffix

        # Option 3: Parent directory with mode suffix
        options[f"Parent directory '{suffix}'"] = parent_dir / suffix

    # Always add custom path option
    options["Custom path (enter manually)"] = None

    return options


def select_output_directory(output_options: Dict[str, Path], source_path: Path) -> Path:
    """Select output directory using arrow keys.

    Args:
        output_options: Dictionary of output options
        source_path: The source path for reference

    Returns:
        Selected output path
    """
    import readchar
    from rich.panel import Panel

    # Get options as list for indexed access
    descriptions = list(output_options.keys())
    paths = list(output_options.values())

    # Default selection
    selected_index = 0

    # Function to render the output directory selection screen
    def render_selection():
        console.clear()
        console.print("\n[bold]Output Directory Selection[/bold]")
        console.print("Use [blue]↑/↓[/blue] arrow keys to navigate, [blue]Enter[/blue] to select\n")
        console.print(f"[yellow]Source:[/yellow] {source_path}\n")

        for i, (desc, path) in enumerate(zip(descriptions, paths)):
            content = f"[bold white]{desc}[/bold white]"
            if path:
                content += f"\n[blue]{path}[/blue]"

            if i == selected_index:
                console.print(Panel(content, border_style="green"))
            else:
                console.print(Panel(content, border_style="blue"))

    # Interactive loop
    while True:
        render_selection()

        # Get keyboard input
        key = readchar.readkey()

        # Handle navigation keys
        if key == readchar.key.UP and selected_index > 0:
            selected_index -= 1
        elif key == readchar.key.DOWN and selected_index < len(descriptions) - 1:
            selected_index += 1
        elif key == readchar.key.ENTER:
            selected_path = paths[selected_index]

            # Handle custom path option
            if selected_path is None:
                console.print("\n[bold]Custom Output Path:[/bold]")
                output_path_str = Prompt.ask("Enter output directory")
                selected_path = Path(output_path_str).expanduser().resolve()

            # Validate the selected path
            if is_valid_output_path(selected_path, source_path):
                return selected_path

            # If invalid, show error and continue loop
            continue

    # This should never be reached, but just in case
    return Path(str(source_path.parent / "output")).expanduser().resolve()


def is_valid_output_path(output_path: Path, source_path: Path) -> bool:
    """Validate output path to prevent potential issues.

    Args:
        output_path: The output path to validate
        source_path: The source path for reference

    Returns:
        True if the output path is valid, False otherwise
    """
    # Check if output is a subdirectory of source (could cause infinite recursion)
    if source_path.is_dir() and output_path.is_relative_to(source_path):
        should_continue = Confirm.ask(
            f"[yellow]Warning: Output directory '{output_path}' is inside source directory. "
            f"This could cause recursive processing. Continue anyway?[/yellow]",
            default=False,
        )
        return should_continue

    # Check if output path already exists and contains files
    if output_path.exists() and any(output_path.iterdir()):
        should_continue = Confirm.ask(
            f"[yellow]Warning: Output directory '{output_path}' already exists and contains files. "
            f"Files may be overwritten. Continue?[/yellow]",
            default=True,
        )
        return should_continue

    return True


def configure_advanced_options(config_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Configure advanced options like caching and rate limiting."""
    options = {}

    # Use values from config if available
    if config_data:
        if "skip_existing" in config_data:
            options["skip_existing"] = config_data["skip_existing"]
        if "use_cache" in config_data:
            options["use_cache"] = config_data["use_cache"]
        if "cache_ttl" in config_data:
            options["cache_ttl"] = config_data["cache_ttl"]
        if "db_path" in config_data:
            options["db_path"] = config_data["db_path"]
        if "workers" in config_data:
            options["workers"] = config_data["workers"]

    # If we have all required options from config, return them
    required_options = ["skip_existing", "use_cache", "db_path", "workers"]
    if all(opt in options for opt in required_options):
        # If using cache, make sure we have cache_ttl
        if options["use_cache"] and "cache_ttl" not in options:
            options["cache_ttl"] = 86400  # Default 24 hours
        console.print("[green]Using advanced options from config file[/green]")
        return options

    # Otherwise ask interactively for missing options
    console.print("\n[bold]Advanced Options:[/bold]")

    # Configure skip existing
    if "skip_existing" not in options:
        options["skip_existing"] = Confirm.ask("Skip existing files?", default=True)

    # Configure caching
    if "use_cache" not in options:
        options["use_cache"] = Confirm.ask("Enable translation cache?", default=True)

    if options["use_cache"] and "cache_ttl" not in options:
        options["cache_ttl"] = int(Prompt.ask("Cache TTL in seconds", default="86400"))

    # Configure database path
    if "db_path" not in options:
        default_db = "~/.transphrase/transphrase.db"
        options["db_path"] = Prompt.ask("Database path", default=default_db)

    # Configure threading
    if "workers" not in options:
        default_threads = os.cpu_count() or 4
        options["workers"] = int(
            Prompt.ask("Max threads for processing", default=str(default_threads))
        )

    return options


def select_plugins(config_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Select plugins to use for translation."""
    from transphrase.plugins.plugin_setup import get_available_plugins, setup_plugin_directories

    # Make sure plugin directories exist
    setup_plugin_directories()

    # Get available plugins
    prompt_templates, processors = get_available_plugins()

    plugins_config = {}

    # Check if we have plugins from config
    if config_data and "plugins" in config_data:
        plugins_config = config_data["plugins"]
        console.print("[green]Using plugins configuration from config file[/green]")
        return plugins_config

    # If we have no plugins, return empty config
    if not prompt_templates and not processors:
        console.print("[yellow]No plugins available. Using default configuration.[/yellow]")
        return {}

    # Ask user if they want to use plugins
    console.print("\n[bold]Plugin Selection:[/bold]")
    use_plugins = Confirm.ask("Do you want to use any plugins?", default=False)

    if not use_plugins:
        return {}

    # Select prompt template if available
    if prompt_templates:
        console.print("\n[bold]Available Prompt Templates:[/bold]")
        for i, template in enumerate(prompt_templates):
            console.print(f"[blue]{i+1}.[/blue] {template['name']}: {template['description']}")

        use_prompt_template = Confirm.ask("Use a custom prompt template?", default=False)

        if use_prompt_template:
            template_choices = [str(i + 1) for i in range(len(prompt_templates))]
            template_idx = (
                int(Prompt.ask("Select prompt template", choices=template_choices, default="1")) - 1
            )

            plugins_config["prompt_template"] = prompt_templates[template_idx]["name"]

    # Select processor modules if available
    if processors:
        console.print("\n[bold]Available Processor Modules:[/bold]")
        for i, processor in enumerate(processors):
            console.print(f"[blue]{i+1}.[/blue] {processor['name']}: {processor['description']}")

        use_processor = Confirm.ask("Use text processor modules?", default=False)

        if use_processor:
            processor_choices = [str(i + 1) for i in range(len(processors))]
            selected_processors = []

            while True:
                processor_idx = int(
                    Prompt.ask(
                        "Select processor (0 to finish)",
                        choices=["0"] + processor_choices,
                        default="0",
                    )
                )

                if processor_idx == 0:
                    break

                selected_name = processors[processor_idx - 1]["name"]
                if selected_name not in selected_processors:
                    selected_processors.append(selected_name)

                console.print(
                    f"[green]Selected processors: {', '.join(selected_processors)}[/green]"
                )

            if selected_processors:
                plugins_config["processors"] = selected_processors

    return plugins_config


def select_series(config_data: Optional[Dict[str, Any]] = None) -> Optional[str]:
    """
    Select a series for context tracking.

    Args:
        config_data: Optional configuration data

    Returns:
        Selected series ID or None
    """
    from transphrase.cache.series_context import SeriesContext

    # Check config file first
    if config_data and "series_id" in config_data and config_data["series_id"]:
        series_id = config_data["series_id"]

        # Verify the series exists
        series_context = SeriesContext()
        series_list = series_context.get_series_list()
        if any(s["series_id"] == series_id for s in series_list):
            series_info = next(s for s in series_list if s["series_id"] == series_id)
            console.print(f"[green]Using series from config: {series_info['name']}[/green]")
            return series_id
        else:
            console.print(f"[yellow]Series ID in config not found: {series_id}[/yellow]")

    # Ask if user wants to use series context
    console.print("\n[bold]Series Context:[/bold]")
    use_series = Confirm.ask("Use series context for consistency?", default=False)

    if not use_series:
        return None

    series_context = SeriesContext()
    series_list = series_context.get_series_list()

    if not series_list:
        console.print("[yellow]No series found. Creating new series.[/yellow]")

        # Create new series
        name = Prompt.ask("Series name")
        description = Prompt.ask("Description (optional)", default="")

        series_id = series_context.create_series(name, description)
        console.print(f"[green]Series created with ID: {series_id}[/green]")

        return series_id

    # Offer options
    console.print("\n[bold]Select Series:[/bold]")
    console.print("[blue]1.[/blue] Create new series")

    for i, series in enumerate(series_list, 2):
        console.print(f"[blue]{i}.[/blue] {series['name']} - {series['description'][:50]}")

    choices = [str(i) for i in range(1, len(series_list) + 2)]
    choice = Prompt.ask("Select option", choices=choices, default="1")
    choice = int(choice)

    if choice == 1:
        # Create new series
        name = Prompt.ask("Series name")
        description = Prompt.ask("Description (optional)", default="")

        series_id = series_context.create_series(name, description)
        console.print(f"[green]Series created with ID: {series_id}[/green]")

        return series_id
    else:
        # Return existing series
        return series_list[choice - 2]["series_id"]


def build_config(
    save_to_file: bool = True, overwrite_config: bool = False, auto_detect_language: bool = True
) -> TranslationConfig:
    """
    Build configuration from config file, user input and environment variables.

    Args:
        save_to_file: Whether to save the configuration to file
        overwrite_config: Whether to overwrite existing configuration

    Returns:
        TranslationConfig object
    """
    # Skip loading existing config if overwrite_config is True
    config_data = None if overwrite_config else load_config_from_file()

    # Get credentials and initialize API handler
    api_key, base_url = get_api_credentials(config_data)
    temp_api_handler = APIHandler(api_key=api_key, base_url=base_url)

    # Get model and mode
    selected_model = select_model(temp_api_handler, config_data)
    selected_mode = select_mode(config_data)

    # Only ask for languages in translate mode
    if selected_mode == "translate":
        source_language, target_language = select_languages(config_data, auto_detect_language)
        selected_polish_style = "standard"  # Default for translate mode
    else:
        # For polish mode, use default values or from config without prompting
        if config_data and "source_language" in config_data and "target_language" in config_data:
            source_language = config_data["source_language"]
            target_language = config_data["target_language"]
        else:
            # Default values
            source_language = "English"  # Default source for polish mode
            target_language = "English"  # Polish mode typically works within one language

        # Ask for polish style in polish mode
        selected_polish_style = select_polish_style(config_data)

    # Get paths
    source_path, output_path = configure_paths(config_data, selected_mode)

    # Create system prompt based on selected mode
    if selected_mode == "translate":
        system_prompt = TRANSLATION_PROMPT_TEMPLATE.format(
            source_language=source_language or "auto-detected", target_language=target_language
        )
    else:  # polish mode
        # Get language-specific guidance
        language_guidance = LANGUAGE_SPECIFIC_POLISH.get(target_language, "")

        # Get style-specific guidance
        style_guidance = POLISH_STYLE_PRESETS.get(
            selected_polish_style, POLISH_STYLE_PRESETS["standard"]
        )

        # Combine language and style guidance
        combined_guidance = f"{style_guidance}\n{language_guidance}"

        # Format the polish prompt template with the target language and combined guidance
        system_prompt = POLISH_PROMPT_TEMPLATE.format(
            target_language=target_language, style_guidance=combined_guidance
        )

    # Get advanced options
    advanced_options = configure_advanced_options(config_data)

    # Select plugins
    plugins_config = select_plugins(config_data)

    # If a custom prompt template is selected, use it
    if plugins_config and "prompt_template" in plugins_config:
        from transphrase.plugins.plugin_manager import PluginManager

        plugin_manager = PluginManager()

        template_name = plugins_config["prompt_template"]
        custom_prompt = plugin_manager.create_prompt_template(
            template_name,
            source_language=source_language,
            target_language=target_language,
        )

        if custom_prompt:
            console.print(f"[green]Using custom prompt template: {template_name}[/green]")
            system_prompt = custom_prompt
        else:
            console.print(
                f"[yellow]Failed to load prompt template '{template_name}'. Using default prompt.[/yellow]"
            )

    # Select series for context tracking
    series_id = select_series(config_data)

    # Build config object
    config = TranslationConfig(
        api_key=api_key,
        base_url=base_url,
        model=selected_model,
        system_prompt=system_prompt,
        mode=selected_mode,
        source_language=source_language,
        target_language=target_language,
        polish_style=selected_polish_style,  # Add polish style to config
        source_dir=source_path,
        output_dir=output_path,
        skip_existing=advanced_options.get("skip_existing", True),
        workers=advanced_options.get("workers", os.cpu_count() or 4),
        use_cache=advanced_options.get("use_cache", True),
        cache_ttl=advanced_options.get("cache_ttl", 86400),
        db_path=advanced_options.get("db_path", "~/.transphrase/transphrase.db"),
        plugin_dirs=[str(p) for p in Path("~/.transphrase/plugins").expanduser().glob("*")],
        series_id=series_id,
        auto_detect_language=auto_detect_language,
    )

    # Add plugin configuration
    if plugins_config:
        setattr(config, "plugins", plugins_config)

    # Save configuration for future use if requested
    if save_to_file and (overwrite_config or not config_data):
        should_save = Confirm.ask("\nSave this configuration for future use?", default=True)
        if should_save:
            # Add plugins to the saved config
            config_dict = {
                "api_key": config.api_key,
                "base_url": config.base_url,
                "model": config.model,
                # "mode": config.mode,
                "source_language": config.source_language,
                "target_language": config.target_language,
                "polish_style": config.polish_style,  # Save polish style to config
                # "source_dir": str(config.source_dir),
                # "output_dir": str(config.output_dir),
                "skip_existing": config.skip_existing,
                "workers": config.workers,
                "use_cache": config.use_cache,
                "cache_ttl": config.cache_ttl,
                "db_path": config.db_path,
                "plugins": plugins_config,
                "series_id": series_id,
            }

            # Save to file
            try:
                with open(CONFIG_FILE, "w") as f:
                    json.dump(config_dict, f, indent=2)
                console.print(f"[green]Configuration saved to {CONFIG_FILE}[/green]")
            except Exception as e:
                console.print(f"[yellow]Warning: Failed to save config file: {e}[/yellow]")

    return config

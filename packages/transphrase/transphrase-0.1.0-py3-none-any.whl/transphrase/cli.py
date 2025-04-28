"""Command-line interface for TransPhrase."""

import logging
import os
import sys
from pathlib import Path

from rich.console import Console
from rich.logging import RichHandler
from rich.prompt import Confirm, Prompt

from transphrase.api.handler import APIHandler
from transphrase.cache.translation_cache import TranslationCache
from transphrase.core.config import (
    DEFAULT_MODEL,
    DEFAULT_POLISH_PROMPT,
    DEFAULT_TRANSLATION_PROMPT,
    DEFAULT_WORKERS,
    TranslationConfig,
)
from transphrase.core.file_processor import FileProcessor
from transphrase.database.models import DBManager
from transphrase.plugins.plugin_manager import PluginManager
from transphrase.rate_limiting.rate_limiter import AdaptiveRateLimiter
from transphrase.ui.model_selector import ModelSelector

# Setup logging with Rich
logger = logging.getLogger("translator")
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="%H:%M:%S",
    handlers=[RichHandler(rich_tracebacks=True, show_time=True)],
)
console = Console()


def get_config() -> TranslationConfig:
    """
    Get application configuration from user input and environment

    Returns:
        TranslationConfig object
    """
    console.print("[bold green]Webnovel Translator & Rephraser[/bold green]\n")

    # Get source directory
    src = Path(
        Prompt.ask("Enter source directory (root of 'text/Chapter...')", default="text/Chapter1")
    ).expanduser()

    while not src.is_dir():
        console.print(f"[red]Directory '{src}' does not exist.[/red]")
        src = Path(Prompt.ask("Enter a valid source directory")).expanduser()

    # Get output directory
    output_folder_name = Prompt.ask(
        "Enter the name of the output folder inside 'AITL'", default="translations"
    )
    out = Path.home() / "AITL" / output_folder_name
    out.mkdir(parents=True, exist_ok=True)

    # Get API key
    api_key = os.getenv("MASTER_API_KEY")
    if not api_key:
        api_key = Prompt.ask("Enter API key", password=True)
        if not api_key:
            console.print("[red]API key is required.[/red]")
            sys.exit(1)

    # Initialize API client and model selector
    api_handler = APIHandler(api_key=api_key)
    model_selector = ModelSelector(api_handler, default_model=DEFAULT_MODEL)

    # Get model
    console.print("[bold]Select a model for translation:[/bold]")
    selected_model = model_selector.select_model()
    console.print(f"[green]Selected model: {selected_model}[/green]")

    # Get prompt type
    prompt_type = Prompt.ask(
        "Choose prompt type (tl for translation, pl for polishing)",
        choices=["tl", "pl"],
        default="tl",
    )

    # Ask for advanced options
    console.print("\n[bold]Advanced Options:[/bold]")
    use_cache = Confirm.ask("Use translation caching?", default=True)

    # Initialize plugin manager and show available plugins
    plugin_manager = PluginManager()
    if plugin_manager.prompt_templates:
        console.print("\n[bold]Available Prompt Templates:[/bold]")
        for template in plugin_manager.list_prompt_templates():
            console.print(f"- {template['name']}: {template['description']}")

    # Allow custom prompt template selection
    use_custom_template = False
    if plugin_manager.prompt_templates and Confirm.ask(
        "Use custom prompt template?", default=False
    ):
        use_custom_template = True
        template_name = Prompt.ask(
            "Enter template name", choices=list(plugin_manager.prompt_templates.keys())
        )
        template_class = plugin_manager.get_prompt_template(template_name)
        if template_class:
            system_prompt = template_class.get_system_prompt()
        else:
            console.print("[yellow]Template not found, using default.[/yellow]")
            system_prompt = (
                DEFAULT_TRANSLATION_PROMPT if prompt_type == "tl" else DEFAULT_POLISH_PROMPT
            )
    else:
        system_prompt = DEFAULT_TRANSLATION_PROMPT if prompt_type == "tl" else DEFAULT_POLISH_PROMPT

    # Get worker count and skip setting
    workers = int(Prompt.ask("Number of parallel workers", default=str(DEFAULT_WORKERS)))
    skip_existing = Confirm.ask("Skip existing translations?", default=True)

    # Create and return enhanced config
    return TranslationConfig(
        api_key=api_key,
        model=selected_model,
        system_prompt=system_prompt,
        workers=workers,
        skip_existing=skip_existing,
        source_dir=src,
        output_dir=out,
        use_cache=use_cache,
        plugin_dirs=[],  # Use default plugin directories
    )


def main() -> None:
    """Main application entry point"""
    try:
        # Get configuration
        config = get_config()

        # Initialize components
        # Setup cache if enabled
        cache = None
        if config.use_cache:
            cache = TranslationCache(ttl=config.cache_ttl)

        # Setup rate limiter
        rate_limiter = AdaptiveRateLimiter(config=config.rate_limit_config)

        # Setup database manager
        db_manager = DBManager(config.db_path)

        # Initialize API handler with new components
        api_handler = APIHandler(
            api_key=config.api_key, base_url=config.base_url, cache=cache, rate_limiter=rate_limiter
        )

        # Initialize file processor with database integration
        file_processor = FileProcessor(config, api_handler, db_manager)

        # Process files
        file_processor.process_files()

    except KeyboardInterrupt:
        console.print("\n[yellow]Operation canceled by user.[/yellow]")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

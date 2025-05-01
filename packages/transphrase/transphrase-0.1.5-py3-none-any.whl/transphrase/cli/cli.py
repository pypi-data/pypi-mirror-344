"""Command-line interface for TransPhrase"""

import logging
import sys
from typing import Any

import click
from rich.console import Console

from transphrase.core.config_manager import build_config
from transphrase.core.container import Container

logger = logging.getLogger("translator")
console = Console()

__all__ = ["main"]


@click.group()
@click.version_option()
@click.pass_context
def cli(ctx: click.Context) -> None:
    """TransPhrase - AI-powered translation tool"""
    ctx.ensure_object(dict)


@cli.group()
@click.option(
    "--no-save-config", is_flag=True, help="Don't save configuration after interactive setup"
)
@click.option("--overwrite-config", is_flag=True, help="Overwrite existing configuration file")
@click.option("--no-auto-detect", is_flag=True, help="Disable automatic source language detection")
@click.pass_context
def translate(
    ctx: click.Context, no_save_config: bool, overwrite_config: bool, no_auto_detect: bool
) -> None:
    """Translation processing commands group

    Handles configuration setup for translation operations.
    """
    ctx.obj["config"] = build_config(
        save_to_file=not no_save_config,
        overwrite_config=overwrite_config,
        auto_detect_language=not no_auto_detect,
    )


@cli.command()
@click.option("--series-manager", is_flag=True, help="Launch series management interface")
def series(series_manager: bool) -> None:
    """Manage translation series and terminology"""
    if series_manager:
        from transphrase.cli.series_manager import SeriesManager

        SeriesManager().run()


def main() -> None:
    """Main entry point for CLI"""
    try:
        cli(obj={})
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation canceled by user.[/yellow]")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@translate.command()
@click.pass_context
def process_files(ctx: click.Context) -> None:
    """Process translation files using pre-configured settings"""
    Container(config=ctx.obj["config"]).file_processor.process_files()


if __name__ == "__main__":
    main()

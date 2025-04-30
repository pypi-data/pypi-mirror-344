"""Command-line interface for TransPhrase"""

import argparse
import logging
import sys

from rich.console import Console

from transphrase.core.config_manager import build_config
from transphrase.core.container import Container

logger = logging.getLogger("translator")
console = Console()


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="TransPhrase - AI-powered translation tool")
    parser.add_argument(
        "--no-save-config",
        action="store_true",
        help="Don't save the configuration after interactive setup",
    )
    parser.add_argument(
        "--overwrite-config",
        action="store_true",
        help="Overwrite existing configuration file (if any)",
    )
    parser.add_argument(
        "--series-manager",
        action="store_true",
        help="Launch the series manager for maintaining character and terminology consistency",
    )
    parser.add_argument(
        "--no-auto-detect",
        action="store_true",
        help="Disable automatic source language detection",
    )
    return parser.parse_args()


def main() -> None:
    """Main application entry point"""
    try:
        # Parse command line arguments
        args = parse_args()

        # Handle series manager if requested
        if args.series_manager:
            from transphrase.cli.series_manager import SeriesManager

            series_manager = SeriesManager()
            series_manager.run()
            return

        # Get configuration
        config = build_config(
            save_to_file=not args.no_save_config,
            overwrite_config=args.overwrite_config,
            auto_detect_language=not args.no_auto_detect,
        )

        # Initialize container with dependencies
        container = Container(config=config)

        # Process files
        container.file_processor.process_files()

    except KeyboardInterrupt:
        console.print("\n[yellow]Operation canceled by user.[/yellow]")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()

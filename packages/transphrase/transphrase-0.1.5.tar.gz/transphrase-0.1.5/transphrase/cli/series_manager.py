"""Series management CLI for TransPhrase."""

import csv
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table
from rich.text import Text

from transphrase.cache.series_context import SeriesContext

console = Console()


class SeriesManager:
    """CLI interface for managing translation series."""

    def __init__(self):
        """Initialize the series manager."""
        self.series_context = SeriesContext()

    def run(self) -> None:
        """Run the series manager interface."""
        while True:
            console.clear()
            console.print("[bold blue]TransPhrase Series Manager[/bold blue]")
            console.print("Maintain consistency across documents in a series\n")

            options = [
                "List all series",
                "Create new series",
                "Manage existing series",
                "Import/Export glossary",
                "Return to main menu",
            ]

            for i, option in enumerate(options, 1):
                console.print(f"[blue]{i}.[/blue] {option}")

            choice = IntPrompt.ask(
                "Select an option", choices=[str(i) for i in range(1, len(options) + 1)]
            )

            if choice == 1:
                self.list_series()
            elif choice == 2:
                self.create_series()
            elif choice == 3:
                self.manage_series()
            elif choice == 4:
                self.import_export_glossary()
            elif choice == 5:
                break

    def list_series(self) -> None:
        """List all available series."""
        series_list = self.series_context.get_series_list()

        if not series_list:
            console.print("[yellow]No series found.[/yellow]")
            input("\nPress Enter to continue...")
            return

        console.print("[bold]Available Series:[/bold]")
        table = Table(show_header=True)
        table.add_column("ID", style="dim")
        table.add_column("Name", style="bold")
        table.add_column("Description")
        table.add_column("Last Updated", style="dim")

        for series in series_list:
            import datetime

            updated = datetime.datetime.fromtimestamp(series["updated_at"]).strftime(
                "%Y-%m-%d %H:%M"
            )
            table.add_row(
                series["series_id"][:8] + "...",
                series["name"],
                (
                    series["description"][:50] + "..."
                    if len(series["description"]) > 50
                    else series["description"]
                ),
                updated,
            )

        console.print(table)
        input("\nPress Enter to continue...")

    def create_series(self) -> None:
        """Create a new series."""
        console.print("[bold]Create New Series[/bold]")

        name = Prompt.ask("Series name")
        description = Prompt.ask("Description (optional)", default="")

        series_id = self.series_context.create_series(name, description)

        console.print(f"[green]Series created successfully with ID: {series_id}[/green]")

        if Confirm.ask("Would you like to add characters or terminology now?"):
            self.manage_series(series_id)
        else:
            input("\nPress Enter to continue...")

    def manage_series(self, selected_id: Optional[str] = None) -> None:
        """
        Manage an existing series.

        Args:
            selected_id: Optional pre-selected series ID
        """
        # If no series ID provided, let user select one
        if not selected_id:
            series_list = self.series_context.get_series_list()

            if not series_list:
                console.print("[yellow]No series found.[/yellow]")
                input("\nPress Enter to continue...")
                return

            console.print("[bold]Select a Series to Manage:[/bold]")

            for i, series in enumerate(series_list, 1):
                console.print(f"[blue]{i}.[/blue] {series['name']} - {series['description'][:50]}")

            choice = IntPrompt.ask(
                "Select a series", choices=[str(i) for i in range(1, len(series_list) + 1)]
            )

            selected_id = series_list[choice - 1]["series_id"]

        # Get series info
        series_list = self.series_context.get_series_list()
        series_info = next((s for s in series_list if s["series_id"] == selected_id), None)

        if not series_info:
            console.print("[red]Series not found.[/red]")
            input("\nPress Enter to continue...")
            return

        while True:
            console.clear()
            console.print(f"[bold blue]Managing Series: {series_info['name']}[/bold blue]")

            options = [
                "View/Edit Characters",
                "View/Edit Terminology",
                "Export Glossary",
                "Return to previous menu",
            ]

            for i, option in enumerate(options, 1):
                console.print(f"[blue]{i}.[/blue] {option}")

            choice = IntPrompt.ask(
                "Select an option", choices=[str(i) for i in range(1, len(options) + 1)]
            )

            if choice == 1:
                self.manage_characters(selected_id)
            elif choice == 2:
                self.manage_terminology(selected_id)
            elif choice == 3:
                self.export_glossary(selected_id)
            elif choice == 4:
                break

    def manage_characters(self, series_id: str) -> None:
        """
        Manage characters for a series.

        Args:
            series_id: Series ID
        """
        while True:
            console.clear()
            console.print("[bold]Character Management[/bold]")

            characters = self.series_context.get_characters(series_id)

            if characters:
                table = Table(show_header=True)
                table.add_column("Name", style="bold")
                table.add_column("Description")
                table.add_column("Aliases")

                for char in characters:
                    table.add_row(
                        char["name"],
                        (
                            char["description"][:50] + "..."
                            if len(char["description"]) > 50
                            else char["description"]
                        ),
                        ", ".join(char["aliases"][:3])
                        + ("..." if len(char["aliases"]) > 3 else ""),
                    )

                console.print(table)
            else:
                console.print("[yellow]No characters found for this series.[/yellow]")

            options = ["Add New Character", "Edit Existing Character", "Return to Series Menu"]

            for i, option in enumerate(options, 1):
                console.print(f"[blue]{i}.[/blue] {option}")

            choice = IntPrompt.ask(
                "Select an option", choices=[str(i) for i in range(1, len(options) + 1)]
            )

            if choice == 1:
                self.add_character(series_id)
            elif choice == 2:
                if characters:
                    self.edit_character(series_id, characters)
                else:
                    console.print("[yellow]No characters to edit.[/yellow]")
                    input("\nPress Enter to continue...")
            elif choice == 3:
                break

    def add_character(self, series_id: str) -> None:
        """
        Add a new character to the series.

        Args:
            series_id: Series ID
        """
        console.print("[bold]Add New Character[/bold]")

        name = Prompt.ask("Character name")
        description = Prompt.ask("Description (optional)", default="")

        aliases_input = Prompt.ask("Aliases (comma-separated, optional)", default="")
        aliases = [a.strip() for a in aliases_input.split(",")] if aliases_input else []

        self.series_context.add_character(series_id, name, description=description, aliases=aliases)

        console.print(f"[green]Character '{name}' added successfully.[/green]")
        input("\nPress Enter to continue...")

    def edit_character(self, series_id: str, characters: List[Dict[str, Any]]) -> None:
        """
        Edit an existing character.

        Args:
            series_id: Series ID
            characters: List of characters
        """
        console.print("[bold]Edit Character[/bold]")

        for i, char in enumerate(characters, 1):
            console.print(f"[blue]{i}.[/blue] {char['name']}")

        choice = IntPrompt.ask(
            "Select a character to edit", choices=[str(i) for i in range(1, len(characters) + 1)]
        )

        selected_char = characters[choice - 1]

        # Show current values and allow editing
        name = Prompt.ask("Character name", default=selected_char["name"])
        description = Prompt.ask("Description", default=selected_char["description"])

        aliases_default = ", ".join(selected_char["aliases"])
        aliases_input = Prompt.ask("Aliases (comma-separated)", default=aliases_default)
        aliases = [a.strip() for a in aliases_input.split(",")] if aliases_input else []

        # Update character
        self.series_context.add_character(
            series_id,
            name,
            description=description,
            aliases=aliases,
            first_appearance=selected_char["first_appearance"],
        )

        console.print(f"[green]Character '{name}' updated successfully.[/green]")
        input("\nPress Enter to continue...")

    def manage_terminology(self, series_id: str) -> None:
        """Manage terminology for a series."""
        while True:
            console.clear()
            console.print("[bold]Terminology Management[/bold]")

            terminology = self.series_context.get_terminology(series_id)

            if terminology:
                # Add search functionality
                search_query = Prompt.ask("Search terms (leave empty to show all)", default="")

                if search_query:
                    filtered_terms = [
                        t
                        for t in terminology
                        if search_query.lower() in t["source_term"].lower()
                        or search_query.lower() in t["target_term"].lower()
                    ]

                    if not filtered_terms:
                        console.print(f"[yellow]No terms found matching '{search_query}'[/yellow]")
                        terminology_to_display = terminology
                    else:
                        terminology_to_display = filtered_terms
                        console.print(f"[green]Found {len(filtered_terms)} matching terms[/green]")
                else:
                    terminology_to_display = terminology

                # Add category filter
                categories = sorted(set(t.get("category", "general") for t in terminology))
                if len(categories) > 1:
                    console.print("\n[bold]Filter by category:[/bold]")
                    for i, category in enumerate(["All"] + categories, 0):
                        console.print(f"[blue]{i}.[/blue] {category}")

                    cat_choice = IntPrompt.ask(
                        "Select category",
                        choices=[str(i) for i in range(len(categories) + 1)],
                        default="0",
                    )

                    if cat_choice > 0:
                        selected_category = categories[cat_choice - 1]
                        terminology_to_display = [
                            t
                            for t in terminology_to_display
                            if t.get("category", "general") == selected_category
                        ]

                # Display terms with pagination
                page_size = 10
                total_pages = (len(terminology_to_display) + page_size - 1) // page_size
                current_page = 1

                while True:
                    console.clear()
                    console.print("[bold]Terminology Management[/bold]")

                    start_idx = (current_page - 1) * page_size
                    end_idx = min(start_idx + page_size, len(terminology_to_display))

                    table = Table(show_header=True)
                    table.add_column("#", style="dim")
                    table.add_column("Source Term", style="bold")
                    table.add_column("Target Term", style="bold blue")
                    table.add_column("Category")
                    table.add_column("Priority")

                    for i, term in enumerate(
                        terminology_to_display[start_idx:end_idx], start_idx + 1
                    ):
                        table.add_row(
                            str(i),
                            term["source_term"],
                            term["target_term"],
                            term["category"],
                            str(term["priority"]),
                        )

                    console.print(table)
                    console.print(f"Page {current_page}/{total_pages}")

                    if total_pages > 1:
                        console.print("[n]ext/[p]revious page, [m]enu")
                        nav = Prompt.ask("Navigation", choices=["n", "p", "m"], default="m")
                        if nav == "n" and current_page < total_pages:
                            current_page += 1
                            continue
                        elif nav == "p" and current_page > 1:
                            current_page -= 1
                            continue
                        elif nav == "m":
                            break
                    else:
                        break
            else:
                console.print("[yellow]No terminology found for this series.[/yellow]")

            options = [
                "Add New Term",
                "Add Multiple Terms (Batch)",
                "Edit Existing Term",
                "Import Terms from CSV",
                "Return to Series Menu",
            ]

            for i, option in enumerate(options, 1):
                console.print(f"[blue]{i}.[/blue] {option}")

            choice = IntPrompt.ask(
                "Select an option", choices=[str(i) for i in range(1, len(options) + 1)]
            )

            if choice == 1:
                self.add_terminology(series_id)
            elif choice == 2:
                self.add_batch_terminology(series_id)
            elif choice == 3:
                if terminology:
                    self.edit_terminology(series_id, terminology)
                else:
                    console.print("[yellow]No terminology to edit.[/yellow]")
                    input("\nPress Enter to continue...")
            elif choice == 4:
                self.import_terminology_csv(series_id)
            elif choice == 5:
                break

    def add_batch_terminology(self, series_id: str) -> None:
        """Add multiple terms at once."""
        console.print("[bold]Add Multiple Terms[/bold]")
        console.print(
            "Enter one term per line in format: source_term|target_term|category|priority"
        )
        console.print("Example: 灵气|Spiritual Energy|cultivation|5")
        console.print("Press Ctrl+D (or Ctrl+Z on Windows) when finished")

        lines = []
        print("\nStart entering terms:")
        try:
            while True:
                line = input()
                if not line:
                    break
                lines.append(line)
        except EOFError:
            pass

        added = 0
        for line in lines:
            parts = line.split("|")
            if len(parts) >= 2:
                source = parts[0].strip()
                target = parts[1].strip()
                category = parts[2].strip() if len(parts) > 2 else "general"
                try:
                    priority = int(parts[3]) if len(parts) > 3 else 1
                except ValueError:
                    priority = 1

                if source and target:
                    self.series_context.add_terminology(
                        series_id,
                        source,
                        target,
                        description="",
                        category=category,
                        priority=priority,
                    )
                    added += 1

        console.print(f"[green]Added {added} terms to the glossary.[/green]")
        input("\nPress Enter to continue...")

    def import_terminology_csv(self, series_id: str) -> None:
        """Import terminology from CSV file."""
        console.print("[bold]Import Terminology from CSV[/bold]")
        console.print(
            "CSV should have columns: source_term,target_term,category,priority,description,case_sensitive"
        )
        console.print("Only source_term and target_term are required.")

        file_path = Prompt.ask("Path to CSV file")
        file_path = os.path.expanduser(file_path)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                count = 0

                for row in reader:
                    if "source_term" not in row or "target_term" not in row:
                        continue

                    source = row["source_term"].strip()
                    target = row["target_term"].strip()

                    if not source or not target:
                        continue

                    category = row.get("category", "general").strip()

                    try:
                        priority = int(row.get("priority", "1"))
                    except ValueError:
                        priority = 1

                    description = row.get("description", "").strip()

                    self.series_context.add_terminology(
                        series_id,
                        source,
                        target,
                        description=description,
                        category=category,
                        priority=priority,
                    )
                    count += 1

            console.print(f"[green]Imported {count} terms from {file_path}[/green]")
        except Exception as e:
            console.print(f"[red]Error importing CSV: {e}[/red]")

        input("\nPress Enter to continue...")

    def export_glossary(self, series_id: str) -> None:
        """
        Export series glossary to a file.

        Args:
            series_id: Series ID
        """
        console.print("[bold]Export Series Glossary[/bold]")

        # Get series info
        series_list = self.series_context.get_series_list()
        series_info = next((s for s in series_list if s["series_id"] == series_id), None)

        if not series_info:
            console.print("[red]Series not found.[/red]")
            input("\nPress Enter to continue...")
            return

        # Prepare export data
        characters = self.series_context.get_characters(series_id)
        terminology = self.series_context.get_terminology(series_id)

        export_data = {
            "series_info": {
                "name": series_info["name"],
                "description": series_info["description"],
                "id": series_id,
            },
            "characters": characters,
            "terminology": terminology,
        }

        # Get export path
        default_path = f"~/transphrase_{series_info['name'].replace(' ', '_')}_glossary.json"
        export_path = Prompt.ask("Export path", default=default_path)
        export_path = os.path.expanduser(export_path)

        # Export to file
        with open(export_path, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        console.print(f"[green]Glossary exported to {export_path}[/green]")
        input("\nPress Enter to continue...")

    def import_export_glossary(self) -> None:
        """Handle glossary import/export options."""
        console.print("[bold]Glossary Import/Export[/bold]")

        options = [
            "Import glossary to existing series",
            "Import glossary as new series",
            "Return to previous menu",
        ]

        for i, option in enumerate(options, 1):
            console.print(f"[blue]{i}.[/blue] {option}")

        choice = IntPrompt.ask(
            "Select an option", choices=[str(i) for i in range(1, len(options) + 1)]
        )

        if choice == 1:
            self.import_glossary(create_new=False)
        elif choice == 2:
            self.import_glossary(create_new=True)
        else:
            return

    def import_glossary(self, create_new: bool = False) -> None:
        """
        Import glossary from a file.

        Args:
            create_new: Whether to create a new series or import to existing
        """
        console.print("[bold]Import Glossary[/bold]")

        # Get import path
        import_path = Prompt.ask("Import file path (JSON)")
        import_path = os.path.expanduser(import_path)

        try:
            with open(import_path, "r", encoding="utf-8") as f:
                import_data = json.load(f)

            if create_new:
                # Create new series
                series_name = import_data.get("series_info", {}).get("name", "Imported Series")
                description = import_data.get("series_info", {}).get("description", "")

                series_id = self.series_context.create_series(series_name, description)
            else:
                # Select existing series
                series_list = self.series_context.get_series_list()

                if not series_list:
                    console.print("[yellow]No series found. Creating new series.[/yellow]")
                    series_name = import_data.get("series_info", {}).get("name", "Imported Series")
                    description = import_data.get("series_info", {}).get("description", "")
                    series_id = self.series_context.create_series(series_name, description)
                else:
                    console.print("[bold]Select a Series for Import:[/bold]")

                    for i, series in enumerate(series_list, 1):
                        console.print(f"[blue]{i}.[/blue] {series['name']}")

                    choice = IntPrompt.ask(
                        "Select a series", choices=[str(i) for i in range(1, len(series_list) + 1)]
                    )

                    series_id = series_list[choice - 1]["series_id"]

            # Import characters
            for char in import_data.get("characters", []):
                self.series_context.add_character(
                    series_id,
                    char["name"],
                    description=char.get("description", ""),
                    aliases=char.get("aliases", []),
                    relationships=char.get("relationships", {}),
                    first_appearance=char.get("first_appearance", ""),
                )

            # Import terminology
            for term in import_data.get("terminology", []):
                self.series_context.add_terminology(
                    series_id,
                    term["source_term"],
                    term["target_term"],
                    description=term.get("description", ""),
                    category=term.get("category", "general"),
                    priority=term.get("priority", 1),
                )

            console.print("[green]Glossary imported successfully.[/green]")

        except Exception as e:
            console.print(f"[red]Error importing glossary: {e}[/red]")

        input("\nPress Enter to continue...")

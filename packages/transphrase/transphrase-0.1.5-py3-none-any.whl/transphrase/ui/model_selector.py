"""Interactive model selection interface"""

import logging
from typing import List

import readchar
from rich.console import Console
from rich.table import Table
from rich.text import Text

from transphrase.api.handler import APIHandler, ModelInfo
from transphrase.core.config import DEFAULT_MODEL, PAGE_SIZE

logger = logging.getLogger("translator")
console = Console()


class ModelSelector:
    """Interactive model selection with real-time search and navigation"""

    def __init__(self, api_handler: APIHandler, default_model: str = DEFAULT_MODEL):
        """
        Initialize model selector

        Args:
            api_handler: API handler instance for fetching models
            default_model: Default model to use if selection fails
        """
        self.api_handler = api_handler
        self.models_info: List[ModelInfo] = []
        self.models: List[str] = []
        self.default_model = default_model

    def _load_models(self) -> bool:
        """
        Load available models

        Returns:
            True if models were loaded successfully, False otherwise
        """
        self.models_info = self.api_handler.fetch_available_models()

        if not self.models_info:
            console.print("[red]Failed to fetch models. Using default model.[/red]")
            return False

        self.models = [model["id"] for model in self.models_info]
        console.print(f"[green]Found {len(self.models)} available models[/green]")
        return True

    def _filter_models(self, search_term: str) -> List[int]:
        """
        Filter models by search term

        Args:
            search_term: Search string to filter models

        Returns:
            List of indices of matching models
        """
        if not search_term:
            return list(range(len(self.models)))

        filtered_indices: List[int] = []
        search_lower = search_term.lower()

        for i, model_info in enumerate(self.models_info):
            searchable_text = (
                model_info["id"].lower()
                + model_info["description"].lower()
                + str(model_info["capabilities"]).lower()
            )
            if search_lower in searchable_text:
                filtered_indices.append(i)

        return filtered_indices

    def _render_model_table(
        self, filtered_indices: List[int], selected_index: int, page_start: int, page_end: int
    ) -> Table:
        """
        Render a table of models for display

        Args:
            filtered_indices: Indices of models to display
            selected_index: Index of currently selected model
            page_start: Start index of current page
            page_end: End index of current page

        Returns:
            Rich Table object for display
        """
        table = Table(show_header=True, header_style="bold magenta", width=console.width)
        table.add_column("#", style="dim", width=4)
        table.add_column("Model", style="green", width=25, no_wrap=True)
        table.add_column("Description", style="blue", width=40)
        table.add_column("Tokens", style="cyan", width=6)
        table.add_column("Pricing", style="yellow", width=22)
        table.add_column("Capabilities", style="magenta", width=20)

        for i in range(page_start, page_end):
            model_idx = filtered_indices[i]
            model_info = self.models_info[model_idx]

            # Truncate description if too long
            desc = model_info["description"]
            if len(desc) > 40:
                desc = desc[:37] + "..."

            row_style = "reverse" if model_idx == selected_index else ""
            table.add_row(
                str(model_idx + 1),
                Text(model_info["id"], style=row_style),
                Text(desc, style=row_style),
                Text(str(model_info["tokens"]), style=row_style),
                Text(model_info["pricing"], style=row_style),
                Text(model_info["capabilities"], style=row_style),
            )

        return table

    def _render_screen(
        self,
        search_term: str,
        filtered_indices: List[int],
        selected_index: int,
        current_position: int,
    ) -> None:
        """
        Render the current state of the selection screen

        Args:
            search_term: Current search term
            filtered_indices: List of indices of filtered models
            selected_index: Index of currently selected model
            current_position: Current position in filtered list
        """
        console.clear()
        console.print("[bold blue]Model Selection[/bold blue]")
        console.print("Type to search, use ↑/↓ to navigate, Enter to select")
        console.print(f"Press 'q' to use default model: [yellow]{self.default_model}[/yellow]")
        console.print(f"Search: [yellow]{search_term}[/yellow]")

        total_filtered = len(filtered_indices)
        if total_filtered == 0:
            console.print("[yellow]No models match your search.[/yellow]")
            return

        # Calculate page bounds
        page_start = (current_position // PAGE_SIZE) * PAGE_SIZE
        page_end = min(page_start + PAGE_SIZE, total_filtered)

        # Display model table
        table = self._render_model_table(filtered_indices, selected_index, page_start, page_end)
        console.print(table)
        console.print(
            f"Showing {page_start+1}-{page_end} of {total_filtered} matches (from {len(self.models)} total models)"
        )

        # Show details for selected model
        if selected_index in filtered_indices:
            model_info = self.models_info[selected_index]
            console.print("\n[bold]Selected Model Details:[/bold]")
            console.print(f"[green]Model:[/green] {model_info['id']}")
            console.print(f"[blue]Description:[/blue] {model_info['description']}")
            console.print(f"[cyan]Context window:[/cyan] {model_info['tokens']} tokens")
            console.print(f"[yellow]Pricing:[/yellow] {model_info['pricing']}")
            console.print(f"[magenta]Capabilities:[/magenta] {model_info['capabilities']}")

    def select_model(self) -> str:
        """
        Interactive model selection with real-time search and navigation

        Returns:
            Selected model ID
        """
        if not self._load_models():
            logger.warning(f"Failed to load models. Using default model: {self.default_model}")
            return self.default_model

        # Initialize state
        search_term = ""
        filtered_indices = list(range(len(self.models)))
        selected_index = 0

        # Find default model in the list if possible
        if self.default_model in self.models:
            selected_index = self.models.index(self.default_model)

        # Add instructions for default model
        console.print(f"[yellow]Default model is: {self.default_model}[/yellow]")
        console.print("[yellow]Press 'q' or ESC to select the default model[/yellow]")

        while True:
            # Find current position in filtered list
            if selected_index in filtered_indices:
                current_position = filtered_indices.index(selected_index)
            else:
                current_position = 0
                if filtered_indices:
                    selected_index = filtered_indices[0]

            self._render_screen(search_term, filtered_indices, selected_index, current_position)

            # Get keyboard input
            key = readchar.readkey()

            # Debug output to see what key is being received
            # Uncomment for debugging: console.print(f"Key pressed: {repr(key)}")

            # Handle navigation keys
            if key == readchar.key.UP or key == "k":
                if selected_index in filtered_indices:
                    current_pos = filtered_indices.index(selected_index)
                    if current_pos > 0:
                        selected_index = filtered_indices[current_pos - 1]
                elif filtered_indices:
                    selected_index = filtered_indices[-1]

            elif key == readchar.key.DOWN or key == "j":
                if selected_index in filtered_indices:
                    current_pos = filtered_indices.index(selected_index)
                    if current_pos < len(filtered_indices) - 1:
                        selected_index = filtered_indices[current_pos + 1]
                elif filtered_indices:
                    selected_index = filtered_indices[0]

            elif key == readchar.key.ENTER:
                if filtered_indices:
                    selected_model = self.models[selected_index]
                    logger.info(f"User selected model: {selected_model}")
                    return selected_model

            # Add multiple ways to select the default model
            elif key == readchar.key.ESC or key == "\x1b" or key == "q" or key == "Q":
                logger.info(f"User chose to use default model: {self.default_model}")
                return self.default_model

            elif key == readchar.key.BACKSPACE:
                if search_term:
                    search_term = search_term[:-1]
                    filtered_indices = self._filter_models(search_term)

                    if filtered_indices and selected_index not in filtered_indices:
                        selected_index = filtered_indices[0]

            elif len(key) == 1 and key.isprintable():
                search_term += key
                filtered_indices = self._filter_models(search_term)

                if filtered_indices and selected_index not in filtered_indices:
                    selected_index = filtered_indices[0]

            # Handle empty filtered list
            if not filtered_indices:
                search_term = ""
                filtered_indices = list(range(len(self.models)))
                selected_index = 0

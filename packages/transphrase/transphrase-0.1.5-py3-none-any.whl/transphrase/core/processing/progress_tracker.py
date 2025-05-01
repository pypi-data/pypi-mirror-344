"""Progress tracking operations for TransPhrase"""

import statistics
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskID,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)


class ProgressTracker:
    """Handles progress tracking and display"""

    def __init__(self):
        """Initialize progress tracker"""
        self.total_chunks_processed = 0
        self.start_time = time.time()
        self.processed_chunks_rate = []
        self.tasks = {}

    def setup_progress(self, total_files: int, total_chunks: int) -> Progress:
        """
        Set up progress tracking with multiple progress bars

        Args:
            total_files: Total number of files to process
            total_chunks: Total number of chunks to process

        Returns:
            Progress instance with configured tasks
        """
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}[/bold blue]"),
            BarColumn(bar_width=40),
            MofNCompleteColumn(),
            TextColumn("•"),
            TimeElapsedColumn(),
            TextColumn("•"),
            TimeRemainingColumn(),
        )

        # Add progress tasks
        self.file_task = progress.add_task(f"[cyan]Files", total=total_files)
        self.chunk_task = progress.add_task(f"[green]Chunks", total=total_chunks, completed=0)
        self.current_file_task = progress.add_task(f"[yellow]Current: ", visible=False)
        self.eta_task = progress.add_task(f"[magenta]ETA", visible=False)
        self.quality_task = progress.add_task(f"[blue]Overall Quality", visible=False)
        self.completion_task = progress.add_task("[bold]Status", visible=False)
        self.rate_task = progress.add_task("[yellow]Processing Rate", visible=False)

        # Store task references
        self.tasks = {
            "file": self.file_task,
            "chunk": self.chunk_task,
            "current_file": self.current_file_task,
            "eta": self.eta_task,
            "quality": self.quality_task,
            "completion": self.completion_task,
            "rate": self.rate_task,
        }

        return progress

    def update_file_progress(
        self, progress: Progress, files_completed: int, total_files: int
    ) -> None:
        """
        Update file progress

        Args:
            progress: Progress instance
            files_completed: Number of completed files
            total_files: Total number of files
        """
        progress.update(
            self.file_task,
            completed=files_completed,
            total=total_files,
            description=f"[cyan]Files [{files_completed}/{total_files}]",
        )

    def update_chunk_progress(
        self, progress: Progress, chunks_completed: int, total_chunks: int
    ) -> None:
        """
        Update chunk progress

        Args:
            progress: Progress instance
            chunks_completed: Number of completed chunks
            total_chunks: Total number of chunks
        """
        self.total_chunks_processed = chunks_completed
        progress.update(
            self.chunk_task,
            completed=chunks_completed,
            total=total_chunks,
            description=f"[green]Chunks [{chunks_completed}/{total_chunks}]",
        )

    def update_quality_display(
        self, progress: Progress, quality_data: Dict[str, Dict[str, float]], quality_assessor: Any
    ) -> None:
        """
        Update quality display with current quality metrics

        Args:
            progress: Progress instance
            quality_data: Dictionary with quality scores
            quality_assessor: QualityAssessor instance for generating labels
        """
        if not quality_data:
            return

        avg_quality = sum(q["overall"] for q in quality_data.values()) / len(quality_data)
        quality_label = quality_assessor._get_quality_label(avg_quality)

        progress.update(
            self.quality_task,
            description=f"[blue]Overall Quality: {avg_quality:.2f}/10 ({quality_label})",
            completed=avg_quality,
            total=10,
            visible=True,
        )

    def update_processing_rate(self, progress: Progress) -> None:
        """
        Calculate and display the processing rate

        Args:
            progress: Progress instance
        """
        if not self.processed_chunks_rate:
            return

        # Calculate average processing rate (chars per second)
        avg_rate = statistics.mean(self.processed_chunks_rate)

        # Calculate median processing rate to reduce impact of outliers
        median_rate = statistics.median(self.processed_chunks_rate)

        # Show rates in chars/sec and estimated words/min (assuming avg word length of 5 chars)
        words_per_min = (median_rate * 60) / 5

        progress.update(
            self.rate_task,
            description=f"[yellow]Rate: {median_rate:.0f} chars/sec ({words_per_min:.0f} words/min)",
            visible=True,
        )

    def update_eta(self, progress: Progress, chunks_completed: int, total_chunks: int) -> None:
        """
        Update ETA based on current progress

        Args:
            progress: Progress instance
            chunks_completed: Number of completed chunks
            total_chunks: Total number of chunks
        """
        if chunks_completed <= 0:
            return

        elapsed = time.time() - self.start_time

        # Use recent rates for more accurate ETA if we have enough data
        if len(self.processed_chunks_rate) > 5:
            # Use median of the last 5 rates for stability
            recent_rates = self.processed_chunks_rate[-5:]
            rate = statistics.median(recent_rates)
        else:
            # Fall back to overall average rate
            rate = chunks_completed / elapsed if elapsed > 0 else 0

        remaining_chunks = total_chunks - chunks_completed
        eta_seconds = remaining_chunks / rate if rate > 0 else 0

        eta = timedelta(seconds=int(eta_seconds))
        progress.update(self.eta_task, description=f"[magenta]ETA: {eta}", visible=True)

    def update_current_file(
        self, progress: Progress, current_file: Optional[str] = None, status: str = "processing"
    ) -> None:
        """
        Update current file display

        Args:
            progress: Progress instance
            current_file: Current file being processed
            status: Status of the file (processing, completed, etc.)
        """
        if not current_file:
            progress.update(self.current_file_task, visible=False)
            return

        file_name = Path(current_file).name

        if status == "processing":
            description = f"[yellow]Processing: {file_name}"
        elif status == "completed":
            description = f"[green]Completed: {file_name}"
        else:
            description = f"[blue]{status.capitalize()}: {file_name}"

        progress.update(
            self.current_file_task,
            description=description,
            visible=True,
        )

    def update_completion_status(
        self, progress: Progress, status: str, is_visible: bool = True
    ) -> None:
        """
        Update completion status

        Args:
            progress: Progress instance
            status: Status message
            is_visible: Whether to show the status
        """
        progress.update(
            self.completion_task,
            description=status,
            visible=is_visible,
        )

    def update_progress(
        self,
        progress: Progress,
        file_status: Dict[str, Dict[str, int]],
        active_files: Set[str],
        last_processed_file: Optional[str] = None,
        is_complete: bool = False,
    ) -> None:
        """
        Update progress display with current state

        Args:
            progress: Progress instance
            file_status: Dictionary tracking per-file progress
            active_files: Set of currently active files
            last_processed_file: Last processed file path
            is_complete: Whether processing is complete
        """
        # Calculate completion percentages
        total_files = len(file_status)
        completed_files = sum(
            1 for f_stats in file_status.values() if f_stats["chunks"] >= f_stats["total_chunks"]
        )

        total_chunks = sum(f_stats["total_chunks"] for f_stats in file_status.values())
        completed_chunks = sum(f_stats["chunks"] for f_stats in file_status.values())

        # Update main progress bars
        if is_complete:
            # If complete, show everything at 100%
            progress.update(
                self.file_task,
                completed=total_files,
                description="[green]Files [Completed]",
            )
            progress.update(
                self.chunk_task,
                completed=total_chunks,
                description="[green]Chunks [Completed]",
            )
        else:
            # Otherwise show actual progress
            self.update_file_progress(progress, completed_files, total_files)
            self.update_chunk_progress(progress, completed_chunks, total_chunks)

        # Update ETA
        self.update_eta(progress, completed_chunks, total_chunks)

        # Update processing rate
        self.update_processing_rate(progress)

        # Update current file display
        if last_processed_file:
            self.update_current_file(
                progress, last_processed_file, "completed" if is_complete else "processing"
            )

        # Update completion status
        if is_complete:
            self.update_completion_status(progress, "[green]Saving results to files...", True)

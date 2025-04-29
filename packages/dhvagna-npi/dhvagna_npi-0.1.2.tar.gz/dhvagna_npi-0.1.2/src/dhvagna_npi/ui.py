"""
User interface module for Dhvagna-NPI.

This module provides UI components and functions for the command-line interface.
"""

import keyboard
from rich.console import Console
from rich.panel import Panel
from rich import box
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, BarColumn, TextColumn

from .utils import get_available_languages, get_language_codes

def show_help(console):
    """Display help information.
    
    Args:
        console (Console): Rich console object for display
    """
    console.clear()
    
    console.print(Panel(
        Text("Help Menu", style="bold magenta", justify="center"),
        border_style="blue",
        box=box.DOUBLE
    ))
    
    help_table = Table(title="[bold]Keyboard Controls[/bold]", box=box.ROUNDED)
    help_table.add_column("Key", style="cyan")
    help_table.add_column("Action", style="green")
    
    help_table.add_row("k", "Start/Stop recording (or your custom hotkey)")
    help_table.add_row("h", "Show this help")
    help_table.add_row("s", "Settings menu")
    help_table.add_row("v", "View recent transcriptions")
    help_table.add_row("q", "Quit")
    
    console.print(help_table)
    console.print()
    console.print("[bold blue]Press any key to return to the main menu...[/bold blue]")
    
    # Wait for any key press to return
    keyboard.read_event(suppress=True)

def settings_menu(config, console):
    """Display settings menu.
    
    Args:
        config: Configuration object to modify
        console (Console): Rich console object for display
    """
    console.clear()
    
    while True:
        console.print(Panel(
            Text("Settings", style="bold magenta", justify="center"),
            border_style="blue",
            box=box.DOUBLE
        ))
        
        settings_table = Table(box=box.ROUNDED)
        settings_table.add_column("Setting")
        settings_table.add_column("Current Value")
        
        settings_table.add_row("1. Hotkey", config.hotkey)
        settings_table.add_row("2. Language", config.language)
        settings_table.add_row("3. Save Transcriptions", "Yes" if config.save_transcriptions else "No")
        settings_table.add_row("4. Transcription Folder", config.transcription_folder)
        settings_table.add_row("5. Audio Timeout (seconds)", str(config.timeout))
        settings_table.add_row("6. Microphone Sensitivity", str(config.energy_threshold))
        settings_table.add_row("0. Back", "Return to main menu")
        
        console.print(settings_table)
        
        choice = Prompt.ask("Select option", choices=["0", "1", "2", "3", "4", "5", "6"])
        
        if choice == "0":
            break
        elif choice == "1":
            new_hotkey = Prompt.ask("Enter new hotkey")
            if new_hotkey:
                config.hotkey = new_hotkey
        elif choice == "2":
            languages = get_available_languages()
            
            language_table = Table(title="Available Languages")
            language_table.add_column("Option")
            language_table.add_column("Language")
            
            for key, value in languages.items():
                language_table.add_row(key, value)
            
            console.print(language_table)
            lang_choice = Prompt.ask("Select language", choices=list(languages.keys()))
            
            language_codes = get_language_codes()
            config.language = language_codes.get(lang_choice, "en-US")
            
        elif choice == "3":
            config.save_transcriptions = Confirm.ask("Save transcriptions to files?")
        elif choice == "4":
            new_folder = Prompt.ask("Enter new transcription folder path", default=config.transcription_folder)
            if new_folder:
                config.transcription_folder = new_folder
                if not os.path.exists(config.transcription_folder):
                    import os
                    os.makedirs(config.transcription_folder)
        elif choice == "5":
            timeout = Prompt.ask("Enter timeout in seconds (minimum 5)", default=str(config.timeout))
            try:
                timeout_val = int(timeout)
                if timeout_val >= 5:
                    config.timeout = timeout_val
                else:
                    console.print("[bold red]Value must be at least 5 seconds[/bold red]")
            except:
                console.print("[bold red]Invalid input[/bold red]")
        elif choice == "6":
            sensitivity = Prompt.ask("Enter microphone sensitivity (100-1000, lower is more sensitive)", 
                                  default=str(config.energy_threshold))
            try:
                sensitivity_val = int(sensitivity)
                if 100 <= sensitivity_val <= 1000:
                    config.energy_threshold = sensitivity_val
                else:
                    console.print("[bold red]Value must be between 100 and 1000[/bold red]")
            except:
                console.print("[bold red]Invalid input[/bold red]")
        
        config.save()
    
    console.clear()

def view_history(history, console):
    """View transcription history.
    
    Args:
        history (TranscriptionHistory): History object containing transcriptions
        console (Console): Rich console object for display
    """
    console.clear()
    
    console.print(Panel(
        Text("Recent Transcriptions", style="bold magenta", justify="center"),
        border_style="blue",
        box=box.DOUBLE
    ))
    
    # First show in-memory history
    recent = history.get_recent(10)
    
    if recent:
        console.print(Panel("In-memory Transcriptions", border_style="cyan"))
        for i, entry in enumerate(reversed(recent)):
            console.print(Panel(
                entry["text"],
                title=f"[bold blue]{entry['timestamp']}[/bold blue]",
                border_style="green",
                box=box.ROUNDED
            ))
    
    # Then show actual transcription files
    saved_transcripts = history.get_saved_transcriptions(10)
    if saved_transcripts:
        console.print(Panel(f"Transcription Files from {history.config.transcription_folder}", border_style="cyan"))
        for file_name, timestamp, text_content in saved_transcripts:
            console.print(Panel(
                text_content,
                title=f"[bold blue]{timestamp} - {file_name}[/bold blue]",
                border_style="yellow",
                box=box.ROUNDED
            ))
    
    if not recent and not saved_transcripts:
        console.print("[bold yellow]No transcriptions in history[/bold yellow]")
    
    console.print("\n[bold blue]Press any key to continue...[/bold blue]")
    keyboard.read_event()
    console.clear()

def create_progress_bar(console, message, steps=100, speed=0.01):
    """Create and display a progress bar.
    
    Args:
        console (Console): Rich console object for display
        message (str): Message to display with the progress bar
        steps (int): Number of steps in the progress bar
        speed (float): Time to wait between updates (in seconds)
        
    Returns:
        None
    """
    with Progress(
        TextColumn(f"[bold yellow]{message}"),
        BarColumn(),
        expand=True
    ) as progress:
        task = progress.add_task("", total=steps)
        for i in range(steps):
            import time
            time.sleep(speed)
            progress.update(task, advance=1)

def display_header(console, config):
    """Display the application header.
    
    Args:
        console (Console): Rich console object for display
        config: Configuration object
        
    Returns:
        Panel: The header panel object
    """
    header = Panel(
        Text("dhvagna-npi", style="bold magenta", justify="center"),
        title="[bold cyan]Advanced Voice Transcriber[/bold cyan]",
        subtitle=f"[italic]Press '{config.hotkey}' to start/stop, Ctrl+C to quit[/italic]",
        border_style="bright_blue",
        box=box.DOUBLE
    )
    console.print(header)
    return header

def display_controls(console, config, has_transcription=False):
    """Display the control panel.
    
    Args:
        console (Console): Rich console object for display
        config: Configuration object
        has_transcription (bool): Whether there is a transcription to view
    """
    controls = Table.grid(expand=True)
    controls.add_column(style="cyan", justify="center")
    controls.add_column(style="magenta", justify="center")
    controls.add_column(style="yellow", justify="center")
    controls.add_column(style="green", justify="center")
    
    controls.add_row(
        f"['{config.hotkey}'] Record", 
        "['h'] Help", 
        "['s'] Settings",
        "['q'] Quit"
    )
    
    if has_transcription:
        controls.add_row(
            "['v'] History", 
            "", 
            "", 
            ""
        )
    
    console.print(Panel(controls, box=box.ROUNDED))

def display_result(console, text, language):
    """Display transcription result.
    
    Args:
        console (Console): Rich console object for display
        text (str): Transcribed text
        language (str): Language code used for transcription
    """
    from .utils import get_language_name
    
    # Get language name
    lang_name = (get_language_name(language) or "Unknown").lower()
    display_language = f"{lang_name}"
    
    result_panel = Panel(
        text,
        title=f"[bold blue]Transcription Result ({display_language})[/bold blue]",
        border_style="bright_blue",
        box=box.HEAVY
    )
    
    console.print("\n")
    console.print(result_panel)
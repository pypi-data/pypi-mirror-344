"""
Core functionality module for Dhvagna-NPI.

This module contains the main functionality for recording and transcribing audio.
"""

import speech_recognition as sr
import keyboard
import time
import threading

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich import box

from .config import Config
from .history import TranscriptionHistory
from .ui import (
    show_help, settings_menu, view_history, create_progress_bar,
    display_header, display_controls, display_result
)
from .utils import get_language_name

def record_audio(console, recognizer, microphone, config, stop_flag, recording_done):
    """Record audio in a separate thread.
    
    Args:
        console (Console): Rich console object for display
        recognizer: SpeechRecognition recognizer object
        microphone: SpeechRecognition microphone object
        config: Configuration object with settings
        stop_flag: Event to signal stopping recording
        recording_done: Event to signal recording is complete
        
    Returns:
        AudioData or None: Recorded audio data or None if no recording
    """
    audio_data = None
    
    with microphone as source:
        # Adjust for ambient noise
        create_progress_bar(console, "Adjusting for ambient noise...", 10, 0.05)
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        
        # Set parameters based on config
        recognizer.energy_threshold = config.energy_threshold
        recognizer.dynamic_energy_threshold = True
        recognizer.pause_threshold = 0.8
        
        console.print(Panel(
            f"Recording started. Press [bold magenta]'{config.hotkey}'[/bold magenta] to stop.",
            title="[bold green]Recording[/bold green]",
            border_style="green",
            box=box.ROUNDED
        ))
        
        try:
            console.print("[bold cyan]Listening for speech...[/bold cyan]")
            # Record until timeout or speech ends
            audio_data = recognizer.listen(source, timeout=config.timeout, phrase_time_limit=None)
            console.print("[bold green]Speech detected and recorded![/bold green]")
        except sr.WaitTimeoutError:
            console.print("[bold yellow]No speech detected within timeout.[/bold yellow]")
        
    recording_done.set()  # Signal that recording is complete
    return audio_data

def transcribe_audio(audio_data, recognizer, language):
    """Transcribe audio data to text.
    
    Args:
        audio_data: SpeechRecognition audio data object
        recognizer: SpeechRecognition recognizer object
        language (str): Language code for transcription
        
    Returns:
        tuple: (success, text, error_message)
    """
    if not audio_data:
        return False, "", "No audio was recorded"
        
    try:
        # Transcribe the audio with the configured language
        text = recognizer.recognize_google(audio_data, language=language)
        return True, text, ""
    except sr.UnknownValueError:
        return False, "", "Speech was not understood"
    except sr.RequestError as e:
        return False, "", f"Error: {e}"

def run_single_transcription():
    """Run a single transcription session and exit.
    
    This function sets up the application, records audio once,
    transcribes it, and then exits.
    """
    # Load configuration
    config = Config.load()
    
    # Initialize history
    history = TranscriptionHistory(config)
    
    console = Console()
    console.clear()
    
    # Create a fancy header
    header = display_header(console, config)
    
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    # Start recording
    console.print("[bold green]Starting recording...[/bold green]")
    
    # Create flags for thread coordination
    stop_flag = threading.Event()
    recording_done = threading.Event()
    audio_data = None
    
    # Function to monitor for key press in background
    def key_monitor():
        while True:
            try:
                event = keyboard.read_event(suppress=True)
                if event.name and event.name.lower() == config.hotkey.lower() and event.event_type == keyboard.KEY_DOWN:
                    stop_flag.set()
                    break
            except KeyboardInterrupt:
                stop_flag.set()
                break
    
    # Start monitoring for key press in background
    key_thread = threading.Thread(target=key_monitor)
    key_thread.daemon = True
    key_thread.start()
    
    # Function to record audio and return the data
    def audio_recorder():
        nonlocal audio_data
        audio_data = record_audio(console, recognizer, microphone, config, stop_flag, recording_done)
    
    # Start recording in background
    record_thread = threading.Thread(target=audio_recorder)
    record_thread.daemon = True
    record_thread.start()
    
    # Display recording animation
    spinner_styles = ["dots", "dots2", "dots3", "dots4", "arc", "star"]
    spinner_idx = 0
    
    try:
        while not stop_flag.is_set() and not recording_done.is_set():
            console.print(f"Recording [cyan]{spinner_styles[spinner_idx % len(spinner_styles)]}[/cyan]", end="\r")
            spinner_idx += 1
            time.sleep(0.2)
    except KeyboardInterrupt:
        stop_flag.set()
    
    # Wait for recording to finish if key was pressed first
    if stop_flag.is_set() and not recording_done.is_set():
        console.print("[bold yellow]Stopping recording...[/bold yellow]")
        recording_done.wait(timeout=2)
    
    # Clear the animation line
    console.print(" " * 50, end="\r")
    
    # Process audio
    create_progress_bar(console, "Transcribing audio...")
    
    success, text, error_message = transcribe_audio(audio_data, recognizer, config.language)
    
    if success:
        # Add to history
        history.add(text)
        
        # Show the result
        display_result(console, text, config.language)
        
        # Exit after showing transcription
        console.print("[bold green]Transcription complete. Exiting application.[/bold green]")
        time.sleep(1)
    else:
        console.print(Panel(error_message, 
                          style="bold white on red", 
                          border_style="red", 
                          box=box.HEAVY))
        console.print("[bold yellow]Error occurred. Exiting application.[/bold yellow]")
        time.sleep(1)

def run_interactive():
    """Run the application in interactive mode.
    
    This function sets up the application and runs it in a loop,
    allowing the user to record multiple transcriptions, change settings, etc.
    """
    # Load configuration
    config = Config.load()
    
    # Initialize history
    history = TranscriptionHistory(config)
    
    console = Console()
    console.clear()
    
    # Create a fancy header
    header = display_header(console, config)
    
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    last_transcription = ""
    
    # Wrap all operations in a try block to handle Ctrl+C
    try:
        while True:
            # Show control panel
            display_controls(console, config, bool(last_transcription))
            
            # Wait for key press
            key_event = keyboard.read_event(suppress=True)
            key = key_event.name.lower() if key_event.name else ""
            
            # Only respond to valid keys - ignore others
            valid_keys = [config.hotkey.lower(), 'h', 's', 'v', 'q']
            if key not in valid_keys:
                continue
                
            if key == config.hotkey.lower():
                # Start recording
                console.print("[bold green]Starting recording...[/bold green]")
                
                # Create flags for thread coordination
                stop_flag = threading.Event()
                recording_done = threading.Event()
                audio_data = None
                
                # Function to monitor for key press in background
                def key_monitor():
                    while True:
                        try:
                            event = keyboard.read_event(suppress=True)
                            if event.name and event.name.lower() == config.hotkey.lower() and event.event_type == keyboard.KEY_DOWN:
                                stop_flag.set()
                                break
                        except KeyboardInterrupt:
                            stop_flag.set()
                            break
                
                # Start monitoring for key press in background
                key_thread = threading.Thread(target=key_monitor)
                key_thread.daemon = True
                key_thread.start()
                
                # Function to record audio and return the data
                def audio_recorder():
                    nonlocal audio_data
                    audio_data = record_audio(console, recognizer, microphone, config, stop_flag, recording_done)
                
                # Start recording in background
                record_thread = threading.Thread(target=audio_recorder)
                record_thread.daemon = True
                record_thread.start()
                
                # Display recording animation
                spinner_styles = ["dots", "dots2", "dots3", "dots4", "arc", "star"]
                spinner_idx = 0
                
                try:
                    while not stop_flag.is_set() and not recording_done.is_set():
                        console.print(f"Recording [cyan]{spinner_styles[spinner_idx % len(spinner_styles)]}[/cyan]", end="\r")
                        spinner_idx += 1
                        time.sleep(0.2)
                except KeyboardInterrupt:
                    stop_flag.set()
                
                # Wait for recording to finish if key was pressed first
                if stop_flag.is_set() and not recording_done.is_set():
                    console.print("[bold yellow]Stopping recording...[/bold yellow]")
                    recording_done.wait(timeout=2)
                
                # Clear the animation line
                console.print(" " * 50, end="\r")
                
                # Process audio
                create_progress_bar(console, "Transcribing audio...")
                
                success, text, error_message = transcribe_audio(audio_data, recognizer, config.language)
                
                if success:
                    last_transcription = text
                    
                    # Add to history
                    history.add(text)
                    
                    # Show the result
                    display_result(console, text, config.language)
                    
                else:
                    console.print(Panel(error_message, 
                                      style="bold white on red", 
                                      border_style="red", 
                                      box=box.HEAVY))
                    
            elif key == 'h':
                show_help(console)
                console.clear()
                console.print(header)
            elif key == 's':
                settings_menu(config, console)
                console.print(header)
            elif key == 'v':
                view_history(history, console)
                console.print(header)
            elif key == 'q':
                if Confirm.ask("Are you sure you want to quit?"):
                    break
    
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        console.print("\n[bold red]Ctrl+C detected. Exiting dhvagna-npi[/bold red]")

def main(interactive=False):
    """Main entry point for the application.
    
    Args:
        interactive (bool): If True, run in interactive mode, otherwise do a single transcription
    """
    try:
        if interactive:
            run_interactive()
        else:
            run_single_transcription()
    except Exception as e:
        Console().print(f"\n[bold red]Error: {e}[/bold red]")
        Console().print("[bold red]Exited dhvagna-npi[/bold red]")
<div align="center">

# Dhvagna-NPI: Voice Transcription Tool

</div>

<p align="center">
  <img alt="Version" src="https://img.shields.io/badge/version-0.1.3-blue">
  <img alt="Python" src="https://img.shields.io/badge/python-3.7%2B-blue">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green">
  <img alt="PyPI Downloads" src="https://img.shields.io/pypi/dm/dhvagna-npi">
</p>

<p align="center">
  <img src="https://github.com/gnanesh-16/dhvagna-npi/raw/main/assets/banner.jpg" alt="Dhvagna-NPI Banner">
</p>

Official Python package for advanced voice transcription with multi-language support. Dhvagna-NPI offers an end-to-end voice transcription suite for developers building speech recognition applications. You can easily transcribe spoken audio to text in multiple languages with a beautiful command-line interface.

With this package, you can easily perform voice transcription from any Python 3.7+ application by utilizing the provided command-line interface or importing the modules directly. Currently, Dhvagna-NPI supports both quick single transcriptions and interactive sessions with customizable settings.

To learn how to use our package, check out our [documentation](#documentation).

---

## Table of Contents
- [Installation](#installation)
- [Get Started](#get-started)
- [Features](#features)
- [Creating Your First Transcription](#creating-your-first-transcription)
- [Using the Command-Line Interface](#using-the-command-line-interface)
- [Customizing Settings](#customizing-settings)
- [Supported Languages](#supported-languages)
- [Examples](#examples)
  - [Minimal Example](#minimal-example)
  - [Quick Transcribe Example](#quick-transcribe-example)
  - [Custom Settings Example](#custom-settings-example)
  - [Save to File Example](#save-to-file-example)
  - [Multilingual Example](#multilingual-example)
- [Available Methods](#available-methods)
- [Documentation](#documentation)
- [License](#license)

---

## Installation

To install the latest version available:

```bash
pip install dhvagna-npi
```

When using this package in your application, make sure to pin to at least the major version (e.g., `==0.1.*`). This helps ensure your application remains stable and avoids potential issues from breaking changes in future updates.

---

## Get Started

Dhvagna-NPI provides a simple way to transcribe voice to text:

```python
from dhvagna_npi.core import transcribe_audio
import speech_recognition as sr

# Initialize recognizer and microphone
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Record and transcribe
with microphone as source:
    print("Listening... Speak now!")
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)
    success, text, _ = transcribe_audio(audio, recognizer, "en-US")
    if success:
        print(f"Transcription: {text}")
```

---

## Features

- **Multi-language Support**: Transcribe speech in English, Spanish, French, German, Chinese, Hindi, Telugu, and more.
- **Offline Processing**: All processing happens locally - your voice data never leaves your computer.
- **Rich Command-line Interface**: Beautiful terminal UI with the `Rich` library.
- **Customizable Settings**: Adjust language, microphone sensitivity, timeout, and more.
- **Transcription History**: Save and retrieve past transcriptions.
- **Multiple Export Formats**: Save transcriptions as text, JSON, or CSV.

---

## Creating Your First Transcription

```python
from dhvagna_npi.config import Config
from dhvagna_npi.core import run_single_transcription

def main():
    # Run a single transcription and exit
    run_single_transcription()

if __name__ == "__main__":
    main()
```

---

## Using the Command-Line Interface

Dhvagna-NPI provides two CLI modes:

```bash
# Quick mode (single transcription)
dhvagna-npi

# Interactive mode (multiple transcriptions with settings)
dhvagna-npi-interactive
```

### Keyboard Controls

- **k** (or custom hotkey): Start/Stop recording
- **h**: Show help
- **s**: Settings menu
- **v**: View recent transcriptions
- **q**: Quit

---

## Customizing Settings

```python
from dhvagna_npi.config import Config

# Create and customize configuration
config = Config()
config.language = "es-ES"  # Set language to Spanish
config.timeout = 15  # Set recording timeout to 15 seconds
config.energy_threshold = 250  # Set microphone sensitivity
config.save_transcriptions = True  # Enable saving transcriptions
config.transcription_folder = "my_transcriptions"  # Set custom folder

# Save configuration
config.save()
```

---

## Supported Languages

- **English (US)** - `en-US`
- **English (UK)** - `en-GB`
- **Spanish** - `es-ES`
- **French** - `fr-FR`
- **German** - `de-DE`
- **Chinese (Mandarin)** - `zh-CN`
- **Hindi** - `hi-IN`
- **Telugu** - `te-IN`

---

## Examples

### Minimal Example

```python
import speech_recognition as sr
from dhvagna_npi.core import transcribe_audio

# Initialize recognizer and microphone
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Record and transcribe
with microphone as source:
    print("Listening... Speak now!")
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)
    success, text, _ = transcribe_audio(audio, recognizer, "en-US")
    if success:
        print(f"Transcription: {text}")
```

### Quick Transcribe Example

```python
from dhvagna_npi.core import run_single_transcription

# Run a single transcription with default settings
run_single_transcription()
```

### Custom Settings Example

```python
import os
from dhvagna_npi.config import Config
from dhvagna_npi.core import transcribe_audio
import speech_recognition as sr

# Create custom configuration
config = Config()
config.language = "fr-FR"  # French
config.energy_threshold = 250  # More sensitive
config.timeout = 8  # 8 second timeout

# Initialize recognizer with custom settings
recognizer = sr.Recognizer()
recognizer.energy_threshold = config.energy_threshold
microphone = sr.Microphone()

# Record and transcribe
with microphone as source:
    print("Adjusting for ambient noise...")
    recognizer.adjust_for_ambient_noise(source)
    
    print("Listening... Speak now!")
    audio = recognizer.listen(source, timeout=config.timeout)
    
    success, text, _ = transcribe_audio(audio, recognizer, config.language)
    if success:
        print(f"French transcription: {text}")
```

### Save to File Example

```python
import json
import os
import datetime
from dhvagna_npi.core import transcribe_audio
import speech_recognition as sr

def save_as_text(text, language, output_dir="output"):
    """Save transcription as a text file."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"transcription_{timestamp}.txt"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Language: {language}\n\n")
        f.write(text)
        
    return filepath

# Initialize recognizer and microphone
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Record and transcribe
with microphone as source:
    print("Listening...")
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)
    
    success, text, _ = transcribe_audio(audio, recognizer, "en-US")
    if success:
        # Save the transcription
        filepath = save_as_text(text, "en-US")
        print(f"Saved transcription to: {filepath}")
```

### Multilingual Example

```python
from dhvagna_npi.config import Config
from dhvagna_npi.utils import get_language_codes
from dhvagna_npi.core import transcribe_audio
import speech_recognition as sr

# Get available language codes
language_codes = get_language_codes()
print("Available languages:")
for key, language in language_codes.items():
    print(f"{key}: {language}")

# Choose a language code
language = "es-ES"  # Spanish

# Initialize recognizer and microphone
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Record and transcribe
with microphone as source:
    print(f"Recording in {language}...")
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)
    
    success, text, _ = transcribe_audio(audio, recognizer, language)
    if success:
        print(f"Transcription in {language}: {text}")
```

---

## Available Methods

```python
from dhvagna_npi.config import Config
from dhvagna_npi.history import TranscriptionHistory
from dhvagna_npi.utils import get_language_name

# Create a configuration
config = Config()

# Get language name from code
language_name = get_language_name("fr-FR")  # Returns "French"

# Create a history manager
history = TranscriptionHistory(config)

# Add a transcription to history
history.add("This is a test transcription")

# Get recent transcriptions
recent = history.get_recent(5)  # Get last 5 transcriptions
```

---

## Documentation

For more detailed information about Dhvagna-NPI, check out the following resources:

- [GitHub Repository](https://github.com/gnanesh-16/dhvagna-npi)
- [PyPI Package](https://pypi.org/project/dhvagna-npi/)
- Examples in the `examples/` directory.

---

## License

This project is licensed under the MIT License - see the [LICENSE file](./LICENSE) for details.

# LinguaLab

**LinguaLab** is a specialised Python package designed for language processing tasks, including text translation and video transcription. It provides tools for handling multilingual content and audio-to-text conversion, with support for various services and APIs.

## Features

- **Text Translation**:
  - Multi-language text translation
  - Language detection
  - Customisable translation providers
  - Proxy and timeout configuration
- **Video Transcription**:
  - Audio-to-text conversion
  - Support for IBM Watson services
  - File-based transcription output
  - Customisable output formats

---

## Installation Guide

### Dependency Notice

Before installing, please ensure the following dependencies are available on your system:

- **Required Third-Party Libraries**:
  - googletrans
  - ibm-watson
  - ibm-cloud-sdk-core
  - filewise
  - pygenutils

  You can install them via pip:
  
  ```bash
  pip install googletrans ibm-watson ibm-cloud-sdk-core filewise pygenutils
  ```

  Or via Anaconda (recommended channel: `conda-forge`):

  ```bash
  conda install -c conda-forge googletrans ibm-watson ibm-cloud-sdk-core filewise pygenutils
  ```

### Installation Instructions

Install the package using pip:

```bash
pip install lingualab
```

### Package Updates

To stay up-to-date with the latest version of this package, simply run:

```bash
pip install --upgrade lingualab
```

---

## Project Structure

The package is organised into the following components:

- **text_translations.py**: Text translation utilities
  - Multi-language translation
  - Language detection
  - Provider configuration
  - Customisable parameters

- **transcribe_video_files.py**: Video transcription tools
  - Audio-to-text conversion
  - IBM Watson integration
  - File output handling

For detailed version history and changes, please refer to:

- `CHANGELOG.md`: Comprehensive list of changes for each version
- `VERSIONING.md`: Versioning policy and guidelines

## Usage Examples

### Text Translation

```python
from lingualab import text_translations

# Translate text from Spanish to English
translated_text = text_translations.translate_string(
    phrase_or_words="Hola mundo",
    lang_origin="es",
    lang_translation="en"
)

# Detect language of a text
detected_lang = text_translations.translate_string(
    phrase_or_words="Bonjour le monde",
    procedure="detect"
)
```

### Video Transcription

```python
from lingualab import transcribe_video_files

# Transcribe a video file using IBM Watson
transcription = transcribe_video_files.transcribe_video(
    video_file="input.mp4",
    api_key="your_api_key",
    service_url="your_service_url"
)

# Save transcription to file
transcribe_video_files.save_transcription_in_file(
    transcript=transcription,
    relative_path_noext="output_transcription"
)
```

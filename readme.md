## What is it?

Note Extractor is a Python tool for extracting notes from audio files (MP3/WAV) and generating guitar tabs.

## Features

- Extract notes from audio using librosa pitch detection
- Generate ASCII guitar tabs
- Generate PDF guitar tabs with professional formatting
- Support for multiple guitar tunings (Standard, Drop D, Drop C)
- Configurable tempo and notes per line for PDF output

## How to run it:

### Install dependencies:

```bash
pip install -r requirements.txt
```

### Basic usage:

```bash
# Extract notes and generate ASCII tab
python note_extractor_tabs_gen.py song.mp3 --output tab.txt

# Generate PDF tab
python note_extractor_tabs_gen.py song.mp3 --pdf tab.pdf

# Full options
python note_extractor_tabs_gen.py song.mp3 \
    --output tab.txt \
    --pdf tab.pdf \
    --title "My Song Tab" \
    --tempo 120 \
    --tuning standard \
    --notes-per-line 20
```

### Command line options:

- `audio_file`: Path to audio file (MP3/WAV)
- `--output`: Output ASCII tab file
- `--pdf`: Output PDF file
- `--title`: Title for PDF (default: "Guitar Tab")
- `--tempo`: Tempo in BPM (optional)
- `--tuning`: Guitar tuning (standard, drop_d, drop_c)
- `--notes-per-line`: Number of notes per line in PDF (default: 20)

## References:

- [great video on notes extraction by Jeff Heaton](https://www.youtube.com/watch?v=rj9NOiFLxWA)
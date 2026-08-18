## What is it?

Note Extractor is a Python tool for extracting notes from audio files (MP3/WAV) and generating guitar tabs.

## Installation

### Using Pixi (recommended):

```bash
# Install pixi
curl -fsSL https://pixi.sh/install.sh | bash

# Clone and install
git clone https://github.com/BronzeCrab/notes_extractor.git
cd notes_extractor
pixi install
```

### Using pip:

```bash
pip install -r requirements.txt
```

## Usage

### Basic usage:

```bash
# Using pixi
pixi run python note_extractor_tabs_gen.py song.mp3 --output tab.txt

# Or using pip
python note_extractor_tabs_gen.py song.mp3 --output tab.txt
```

### Generate PDF:

```bash
pixi run python note_extractor_tabs_gen.py song.mp3 --pdf tab.pdf
```

### Full options:

```bash
pixi run python note_extractor_tabs_gen.py song.mp3 \
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

## Development

### Run tests:

```bash
pixi run test
```

### Lint:

```bash
pixi run lint
```

### Format:

```bash
pixi run format
```

## FFT Dependencies

- **librosa**: Primary audio analysis library (uses scipy.signal.stft, numpy.fft)
- **numpy**: Fast Fourier Transform (numpy.fft)
- **scipy**: Signal processing (scipy.signal)
- **reportlab**: PDF generation

These libraries work on Windows, macOS, and Linux.

## References:

- [great video on notes extraction by Jeff Heaton](https://www.youtube.com/watch?v=rj9NOiFLxWA)
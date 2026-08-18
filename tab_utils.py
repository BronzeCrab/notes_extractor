"""
Pitch detection and tab generation utilities for notes_extractor.
"""
from pathlib import Path
from typing import Optional

import numpy as np


def detect_peaks(audio_data: np.ndarray, sr: int) -> list[float]:
    """Detect frequency peaks from audio using librosa's piptrack."""
    import librosa
    
    pitches, magnitudes = librosa.piptrack(y=audio_data, sr=sr)
    
    # Get dominant pitch per frame
    peak_freqs = []
    for i in range(pitches.shape[1]):
        freq_idx = magnitudes[:, i].argmax()
        freq = pitches[freq_idx, i]
        if freq > 80.0:  # Filter low frequencies
            peak_freqs.append(freq)
    
    return peak_freqs


def hz_to_note_name(hz: float) -> tuple[str, int]:
    """Convert Hz to note name and octave."""
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    # MIDI note number
    midi = 69 + 12 * (np.log2(hz / 440.0))
    midi_rounded = int(round(midi))
    
    note_idx = midi_rounded % 12
    octave = midi_rounded // 12 - 1
    
    return note_names[note_idx], octave


def freq_to_tab_position(hz: float, tuning: str = "standard") -> Optional[tuple[int, int]]:
    """Convert frequency to guitar string/fret position.
    
    Returns (string_index, fret) or None if not playable.
    """
    # Standard tuning frequencies (low to high)
    standard_strings = [82.41, 110.0, 146.83, 196.0, 246.94, 329.63]
    
    tunings = {
        "standard": standard_strings,
        "drop_d": [73.42, 110.0, 146.83, 196.0, 246.94, 329.63],
        "drop_c": [65.41, 98.0, 130.81, 196.0, 246.94, 329.63],
    }
    
    strings = tunings.get(tuning, standard_strings)
    
    for string_idx, open_hz in enumerate(strings):
        # All 22 frets
        for fret in range(23):
            if fret == 0:
                target_hz = open_hz
            else:
                target_hz = open_hz * (2.0 ** (fret / 12.0))
            
            # Within 5% tolerance
            if abs(hz - target_hz) / target_hz < 0.05:
                return (string_idx + 1, fret)  # 1-indexed string
    
    return None


def generate_ascii_tab(notes: list[tuple[int, int]]) -> str:
    """Generate ASCII guitar tab from list of (string, fret) tuples."""
    # Initialize tab lines
    lines = ["e|--", "B|--", "G|--", "D|--", "A|--", "E|--"]
    
    # Track position per string
    string_pos = {i: 2 for i in range(1, 7)}
    
    for string, fret in notes:
        if 1 <= string <= 6:
            line_idx = 6 - string  # Convert to tab line index
            # Extend line if needed
            while len(lines[line_idx]) < string_pos[string] + 3:
                lines[line_idx] += "-"
            # Place fret marker
            lines[line_idx] = lines[line_idx][:string_pos[string]] + \
                               f"{fret if fret > 9 else f' {fret}'}--"
            string_pos[string] += 3
    
    return "\n".join(lines) + "-"


# Need numpy for hz_to_note_name
import numpy as np
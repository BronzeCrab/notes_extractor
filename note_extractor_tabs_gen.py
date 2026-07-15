#!/usr/bin/env python3
"""
Note Extractor: Extract notes from audio and generate guitar tabs.

Usage:
    python note_extractor_tabs_gen.py <audio_file.mp3|wav> [--tuning STANDARD|DROP_D|DROP_C] [--output TAB_FILE] [--pdf PDF_FILE]
"""
import argparse
import sys
from pathlib import Path

import librosa
import numpy as np

from tab_utils import detect_peaks, freq_to_tab_position, generate_ascii_tab
from pdf_utils import generate_pdf_tab


def main():
    parser = argparse.ArgumentParser(description="Extract guitar notes from audio")
    parser.add_argument("audio_file", type=Path, help="Path to audio file (MP3/WAV)")
    parser.add_argument("--tuning", default="standard", help="Guitar tuning")
    parser.add_argument("--output", type=Path, help="Output tab file (ASCII)")
    parser.add_argument("--pdf", type=Path, help="Output PDF file")
    parser.add_argument("--title", default="Guitar Tab", help="Title for PDF")
    parser.add_argument("--tempo", type=int, help="Tempo in BPM")
    parser.add_argument("--notes-per-line", type=int, default=20, help="Notes per line in PDF")
    args = parser.parse_args()

    if not args.audio_file.exists():
        print(f"Error: {args.audio_file} not found")
        sys.exit(1)

    print(f"Loading {args.audio_file}...")
    y, sr = librosa.load(args.audio_file, sr=None)
    
    print(f"Detecting pitch peaks...")
    frequencies = detect_peaks(y, sr)
    
    # Cluster and deduplicate frequencies
    unique_freqs = []
    for f in frequencies:
        if not unique_freqs or min(abs(f - uf) for uf in unique_freqs) > 5.0:
            unique_freqs.append(f)
    
    print(f"Found {len(unique_freqs)} unique frequencies")
    
    # Convert to tab positions
    tab_notes = []
    for freq in unique_freqs[:30]:  # First 30 notes
        if (pos := freq_to_tab_position(freq, args.tuning)):
            tab_notes.append(pos)
            print(f"  {freq:.1f}Hz -> String {pos[0]}, fret {pos[1]}")
    
    # Generate ASCII tab
    tab = generate_ascii_tab(tab_notes)
    
    print("\n=== Generated Tab ===")
    print(tab)
    
    # Save ASCII tab
    if args.output:
        args.output.write_text(tab)
        print(f"\nASCII tab saved to {args.output}")
    
    # Generate PDF
    if args.pdf:
        print(f"\nGenerating PDF...")
        generate_pdf_tab(
            tab_notes,
            args.pdf,
            title=args.title,
            tuning=args.tuning.capitalize(),
            tempo=args.tempo,
            notes_per_line=args.notes_per_line
        )
        print(f"PDF saved to {args.pdf}")
    
    if not args.output and not args.pdf:
        print("\nTip: Use --output or --pdf to save the tab")


if __name__ == "__main__":
    main()
"""
PDF generation utilities for notes_extractor.
"""
from pathlib import Path
from typing import Optional
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def generate_pdf_tab(
    notes: list[tuple[int, int]], 
    output_path: Path,
    title: str = "Guitar Tab",
    tuning: str = "Standard",
    tempo: Optional[int] = None,
    notes_per_line: int = 20
) -> Path:
    """Generate a PDF guitar tab from list of (string, fret) tuples.
    
    Args:
        notes: List of (string_number, fret_number) tuples
        output_path: Path to save the PDF
        title: Title of the tab
        tuning: Guitar tuning name
        tempo: Tempo in BPM (optional)
        notes_per_line: Number of notes per line
    """
    # Create PDF document
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm
    )
    
    # Create styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center
    )
    
    info_style = ParagraphStyle(
        'Info',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=10
    )
    
    # Build content
    story = []
    
    # Title
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 10))
    
    # Info
    info_text = f"<b>Tuning:</b> {tuning}"
    if tempo:
        info_text += f" | <b>Tempo:</b> {tempo} BPM"
    story.append(Paragraph(info_text, info_style))
    story.append(Spacer(1, 20))
    
    # Generate tab lines
    tab_lines = _generate_tab_lines(notes, notes_per_line)
    
    # Create table for tab
    table_data = []
    for line in tab_lines:
        # Each line is a string like "e|--5- 8-  10---"
        table_data.append([Paragraph(line, styles['Normal'])])
    
    # Create table
    tab_table = Table(table_data, colWidths=[150*mm])
    tab_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
    ]))
    
    story.append(tab_table)
    
    # Build PDF
    doc.build(story)
    
    return output_path


def _generate_tab_lines(
    notes: list[tuple[int, int]], 
    notes_per_line: int = 20
) -> list[str]:
    """Generate ASCII tab lines from notes list."""
    # Initialize tab lines
    lines = [
        "e|",  # High E string
        "B|",
        "G|",
        "D|",
        "A|",
        "e|"   # Low E string
    ]
    
    # Track position per string
    string_pos = {i: 0 for i in range(6)}
    
    # Group notes by line
    note_groups = []
    for i in range(0, len(notes), notes_per_line):
        note_groups.append(notes[i:i + notes_per_line])
    
    # Generate each line
    for group_idx, group in enumerate(note_groups):
        for string, fret in group:
            if 1 <= string <= 6:
                line_idx = 6 - string  # Convert to tab line index (0 = high E)
                
                # Add spacing
                if string_pos[line_idx] > 0:
                    lines[line_idx] += " "
                
                # Add fret number
                if fret == 0:
                    lines[line_idx] += "0 "
                elif fret < 10:
                    lines[line_idx] += f"{fret} "
                else:
                    lines[line_idx] += f"{fret} "
                
                string_pos[line_idx] += 1
        
        # Add separator line between groups
        if group_idx < len(note_groups) - 1:
            separator = " " * (notes_per_line * 3)
            for i in range(6):
                lines[i] += separator
    
    return lines
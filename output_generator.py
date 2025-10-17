# output_generator.py

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

def create_summary_pdf(
    original_filename: str,
    summaries: dict, # Changed from summary_text to summaries (dictionary)
    output_path: str
):
    """Generates a clean, formatted PDF file from a dictionary of summaries."""
    doc = SimpleDocTemplate(output_path)
    styles = getSampleStyleSheet()
    
    # --- Define Styles ---
    styles.add(ParagraphStyle(
        name='TitleStyle',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        spaceAfter=0.3*inch
    ))
    styles.add(ParagraphStyle(
        name='SubheadingStyle',
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        spaceBefore=0.2*inch,
        spaceAfter=0.1*inch
    ))
    styles.add(ParagraphStyle(
        name='BodyStyle',
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=12
    ))

    story = []

    # --- Add the main title ---
    title = f"Factual Summary of: {original_filename}"
    story.append(Paragraph(title, styles['TitleStyle']))

    # --- Iterate through the summaries dictionary ---
    # Define the display order to ensure the PDF is structured logically.
    display_order = ['100', '50', '20', '10', '5']
    
    for ratio in display_order:
        if ratio in summaries:
            summary_text = summaries[ratio]
            
            # Add a subheading for the current ratio
            subheading = f"Summary at 1:{ratio} Ratio"
            story.append(Paragraph(subheading, styles['SubheadingStyle']))
            
            # Add the summary body text
            story.append(Paragraph(summary_text, styles['BodyStyle']))
            story.append(Spacer(1, 0.2*inch))

    try:
        doc.build(story)
        print(f"PDF generation successful.")
    except Exception as e:
        print(f"Error generating PDF: {e}")

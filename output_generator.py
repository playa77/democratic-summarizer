# output_generator.py
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
def create_summary_pdf(original_filename: str, summary_text: str, output_path: str):
    doc = SimpleDocTemplate(output_path)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='TitleStyle', fontName='Helvetica-Bold', fontSize=18, alignment=TA_CENTER, spaceAfter=0.5*inch))
    styles.add(ParagraphStyle(name='BodyStyle', fontName='Helvetica', fontSize=11, leading=14, alignment=TA_JUSTIFY))
    story = [Paragraph(f"Factual Summary of: {original_filename}", styles['TitleStyle']), Paragraph(summary_text, styles['BodyStyle'])]
    doc.build(story)

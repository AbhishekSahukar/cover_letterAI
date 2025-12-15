from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

def generate_pdf(text: str, filename="cover_letter.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=2.5 * cm,
        leftMargin=2.5 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm,
    )

    styles = getSampleStyleSheet()

    letter_style = ParagraphStyle(
        "Letter",
        parent=styles["Normal"],
        fontSize=11,
        leading=16,
        spaceAfter=12,
    )

    story = []

    # Split by blank lines → proper paragraphs
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    for para in paragraphs:
        story.append(Paragraph(para.replace("\n", "<br />"), letter_style))
        story.append(Spacer(1, 12))

    doc.build(story)
    return filename

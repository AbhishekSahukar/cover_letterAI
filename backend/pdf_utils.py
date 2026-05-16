from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

OUTPUT_PATH = "cover_letter.pdf"


def generate_pdf(text: str, filename: str = OUTPUT_PATH) -> str:
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
        spaceAfter=10,
    )

    story = []
    for para in text.split("\n\n"):
        para = para.strip()
        if para:
            story.append(Paragraph(para.replace("\n", "<br />"), letter_style))
            story.append(Spacer(1, 10))

    doc.build(story)
    return filename
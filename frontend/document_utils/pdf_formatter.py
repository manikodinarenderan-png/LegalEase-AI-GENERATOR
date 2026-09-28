from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def format_pdf(text: str, doc_type: str, terms: str) -> bytes:
    output = BytesIO()
    document = SimpleDocTemplate(
        output,
        pagesize=letter,
        rightMargin=0.8 * inch,
        leftMargin=0.8 * inch,
        topMargin=0.8 * inch,
        bottomMargin=0.8 * inch,
    )
    styles = getSampleStyleSheet()
    body_style = ParagraphStyle(
        "LegalDocumentBody",
        parent=styles["BodyText"],
        fontName="Times-Roman",
        fontSize=10.5,
        leading=15,
    )
    story = []

    for line in text.splitlines():
        if line:
            story.append(Paragraph(escape(line), body_style))
        else:
            story.append(Spacer(1, 8))

    document.build(story)
    return output.getvalue()
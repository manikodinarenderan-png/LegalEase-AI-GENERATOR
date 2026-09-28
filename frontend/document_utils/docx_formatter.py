from io import BytesIO

from docx import Document


def format_docx(
    text: str,
    doc_type: str,
    terms: str,
    logo_path: str,
) -> bytes:
    document = Document()
    document.add_heading(doc_type.strip() or "Legal Document", level=1)

    for line in text.splitlines():
        document.add_paragraph(line)

    output = BytesIO()
    document.save(output)
    return output.getvalue()
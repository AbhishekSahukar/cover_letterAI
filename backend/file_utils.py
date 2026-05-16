import io

from fastapi import UploadFile


async def extract_text(file: UploadFile) -> str:
    raw = await file.read()
    filename = (file.filename or "").lower()

    if filename.endswith(".pdf"):
        return _extract_pdf(raw)

    if filename.endswith(".docx"):
        return _extract_docx(raw)

    # Plain text fallback (also handles .txt and pasted content)
    return raw.decode("utf-8", errors="ignore")


def _extract_pdf(data: bytes) -> str:
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(data))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages).strip()


def _extract_docx(data: bytes) -> str:
    from docx import Document

    doc = Document(io.BytesIO(data))
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs).strip()
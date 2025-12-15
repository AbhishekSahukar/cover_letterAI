from fastapi import APIRouter, UploadFile, Form
from llm import generate_cover_letter
from db import SessionLocal, Chat
from file_utils import extract_text
from pdf_utils import generate_pdf
from fastapi.responses import FileResponse
from pydantic import BaseModel

router = APIRouter()

@router.post("/generate")
async def generate(
    message: str = Form(""),
    cv: UploadFile | None = None,
    jd: UploadFile | None = None
):
    db = SessionLocal()
    source_text = ""

    if cv:
        source_text += "\nCV:\n" + await extract_text(cv)

    if jd:
        source_text += "\nJob Description:\n" + await extract_text(jd)

    if not source_text and message.strip():
        source_text = f"Job Description:\n{message}"

    if not source_text:
        return {
            "letter": "Please upload a CV and/or Job Description to generate a cover letter."
        }

    prompt = f"""
    Generate a professional, ATS-friendly cover letter
    based on the following information.
    The tone should be formal and industry-standard.

    {source_text}
    """

    letter = generate_cover_letter(prompt)

    db.add(Chat(role="user", content=source_text[:3000]))
    db.add(Chat(role="assistant", content=letter))
    db.commit()

    return {"letter": letter}

@router.get("/history")
def history():
    db = SessionLocal()
    chats = db.query(Chat).all()
    return [{"role": c.role, "content": c.content} for c in chats]


class DownloadRequest(BaseModel):
    letter: str

@router.post("/download")
def download(req: DownloadRequest):
    path = generate_pdf(req.letter)

    return FileResponse(
        path,
        media_type="application/pdf",
        filename="cover_letter.pdf",
    )

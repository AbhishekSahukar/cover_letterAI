from fastapi import APIRouter, Form, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel

from db import Chat, get_db
from file_utils import extract_text
from llm import generate_cover_letter
from pdf_utils import generate_pdf

router = APIRouter()

PROMPT_TEMPLATE = """\
Write a professional cover letter based on the information below.
The tone should be confident, concise, and tailored to the role.

{source_text}
"""


@router.post("/generate")
async def generate(
    message: str = Form(""),
    cv: UploadFile | None = None,
    jd: UploadFile | None = None,
):
    source_text = ""

    if cv:
        cv_text = await extract_text(cv)
        if cv_text.strip():
            source_text += f"CV / Resume:\n{cv_text}\n\n"

    if jd:
        jd_text = await extract_text(jd)
        if jd_text.strip():
            source_text += f"Job Description:\n{jd_text}\n\n"

    if not source_text and message.strip():
        source_text = f"Job Description:\n{message}\n"

    if not source_text:
        return {
            "letter": (
                "Please upload your CV and/or a Job Description to get started."
            )
        }

    prompt = PROMPT_TEMPLATE.format(source_text=source_text.strip())
    letter = generate_cover_letter(prompt)

    with get_db() as db:
        db.add(Chat(role="user", content=source_text[:3000]))
        db.add(Chat(role="assistant", content=letter))
        db.commit()

    return {"letter": letter}


@router.get("/history")
def history():
    with get_db() as db:
        chats = db.query(Chat).order_by(Chat.id).all()
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
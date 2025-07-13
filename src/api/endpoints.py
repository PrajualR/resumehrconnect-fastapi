from fastapi import APIRouter, UploadFile, File, Form
from src.resumehrconnect.matcher import ResumeMatcher
from src.resumehrconnect.pdf_extract import extract_text, preprocess_resume_text
from src.models.schemas import MatchResponse
from typing import List

router = APIRouter()
matcher = ResumeMatcher()

@router.post("/match", response_model=MatchResponse)
async def match_resumes(
    job_description: str = Form(...),
    files: List[UploadFile] = File(...)
):
    resume_texts = []
    filenames = []

    for file in files:
        content = await file.read()
        text = preprocess_resume_text(extract_text(content, file.filename))
        if not text.strip():
            continue
        if text:
            resume_texts.append(text)
            filenames.append(file.filename)

    results = matcher.match(job_description, resume_texts, filenames)
    return {"results": results}

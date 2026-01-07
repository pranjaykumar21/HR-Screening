from fastapi import APIRouter, UploadFile, File, HTTPException
from uuid import uuid4
from pathlib import Path

from app.schemas.resume import ResumeUploadResponse, ParsedResumeResponse
from app.utils.handler import save_file
from app.services.resume_parser import parse_resume
from app.core.config import UPLOAD_DIR

router = APIRouter(prefix="/api/resume", tags=["Resume"])

@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type not in [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    resume_id = str(uuid4())
    file_ext = Path(file.filename).suffix
    save_path = UPLOAD_DIR / f"{resume_id}{file_ext}"

    save_file(file, save_path)

    return {
        "resume_id": resume_id,
        "status": "uploaded"
    }

@router.post("/parse", response_model=ParsedResumeResponse)
async def parse_uploaded_resume(resume_id: str):
    files = list(UPLOAD_DIR.glob(f"{resume_id}.*"))

    if not files:
        raise HTTPException(status_code=404, detail="Resume not found")

    parsed_data = parse_resume(str(files[0]))
    return parsed_data

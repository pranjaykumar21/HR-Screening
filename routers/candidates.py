from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Candidate
from schemas import CandidateCreate
from llm import parse_resume
from fastapi import UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from io import BytesIO
import pdfplumber
from docx import Document

router = APIRouter(prefix="/candidates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_candidate(data: CandidateCreate, db: Session = Depends(get_db)):
    candidate = Candidate(**data.dict())
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate

@router.post("/{id}/resume")
async def upload_resume(id: int, file: UploadFile, db: Session = Depends(get_db)):
    content = await file.read()  # ✅ always read as bytes

    filename = file.filename.lower()

    # ---------- PARSE FILE ----------
    if filename.endswith(".pdf"):
        text = ""
        with pdfplumber.open(BytesIO(content)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

    elif filename.endswith(".docx"):
        doc = Document(BytesIO(content))
        text = "\n".join([p.text for p in doc.paragraphs])

    elif filename.endswith(".txt"):
        text = content.decode("utf-8", errors="ignore")

    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported resume format. Upload PDF, DOCX, or TXT."
        )

    # ---------- BUSINESS LOGIC ----------
    parsed = parse_resume(text)

    candidate = db.query(Candidate).get(id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    candidate.resume_text = parsed
    db.commit()

    return {"parsed_resume": parsed}


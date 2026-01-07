from fastapi import APIRouter
from pydantic import BaseModel
from llm import parse_resume

router = APIRouter(prefix="/ai")

class ResumeInput(BaseModel):
    resume_text: str

@router.post("/parse-resume")
def ai_parse(data: ResumeInput):
    parsed = parse_resume(data.resume_text)
    return {"parsed_resume": parsed}

from typing import List
from pydantic import BaseModel

class ResumeUploadResponse(BaseModel):
    resume_id: str
    status: str

class ParsedResumeResponse(BaseModel):
    skills: List[str]
    education: List[str]
    experience: List[str]
    projects: List[str]

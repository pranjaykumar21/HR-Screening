from pydantic import BaseModel

class CandidateCreate(BaseModel):
    name: str
    email: str
    skills: str
    experience: int

class JobCreate(BaseModel):
    title: str
    description: str
    skills_required: str

class ApplicationCreate(BaseModel):
    candidate_id: int
    job_id: int

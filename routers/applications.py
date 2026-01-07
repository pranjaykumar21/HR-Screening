from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Application, Candidate, Job
from schemas import ApplicationCreate
from llm import match_candidate_job

router = APIRouter(prefix="/applications")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_application(data: ApplicationCreate, db: Session = Depends(get_db)):
    app = Application(**data.dict())
    db.add(app)
    db.commit()
    db.refresh(app)
    return app

@router.post("/{id}/screen")
def screen_application(id: int, db: Session = Depends(get_db)):
    app = db.query(Application).get(id)

    candidate = db.query(Candidate).get(app.candidate_id)
    job = db.query(Job).get(app.job_id)

    result = match_candidate_job(candidate, job)

    app.status = "screened"
    app.score = 75  # optional fallback score

    db.commit()

    return {
        "application_id": app.id,
        "screening_result": result
    }

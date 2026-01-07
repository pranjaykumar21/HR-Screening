from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Job
from schemas import JobCreate

router = APIRouter(prefix="/jobs")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_job(data: JobCreate, db: Session = Depends(get_db)):
    job = Job(**data.dict())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

@router.get("/")
def list_jobs(db: Session = Depends(get_db)):
    return db.query(Job).all()

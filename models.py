from sqlalchemy import Column, Integer, String, Text, ForeignKey
from database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    skills = Column(Text)
    experience = Column(Integer)
    resume_text = Column(Text)

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    skills_required = Column(Text)

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    status = Column(String, default="applied")
    score = Column(Integer, nullable=True)

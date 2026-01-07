from fastapi import FastAPI
from database import Base, engine
from routers import candidates, jobs, applications, ai

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Recruitment Backend")

app.include_router(candidates.router)
app.include_router(jobs.router)
app.include_router(applications.router)
app.include_router(ai.router)

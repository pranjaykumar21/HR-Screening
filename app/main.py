from fastapi import FastAPI
from app.routes import resume


app = FastAPI(
    title="AI HR Screening Backend",
    version="1.0.0"
)

app.include_router(resume.router)

@app.get("/")
def health_check():
    return {"status": "Backend is running"}

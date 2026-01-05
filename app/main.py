from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title="Resume Parsing Microservice",
    version=settings.VERSION,
)

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": settings.SERVICE_NAME,
        "env": settings.ENV
    }

import json
import redis
import requests
from services.downloader import download_resume
from services.extractor import extract_text
from services.parser import parse_resume
from services.ats_scorer import calculate_ats_score
from config import settings

r = redis.from_url(settings.REDIS_URL)

def process_job(job):
    resume_id = job["resumeId"]
    file_url = job["fileUrl"]

    try:
        path = download_resume(file_url)
        text = extract_text(path)
        parsed = parse_resume(text)
        ats = calculate_ats_score(text)

        payload = {
            "resume_id": resume_id,
            "parsed_data": parsed,
            "ats_score": ats
        }

        requests.post(
            f"{settings.NEST_API_URL}/internal/resumes/processed",
            json=payload,
            headers={"x-service-secret": settings.SERVICE_SECRET}
        )

    except Exception as e:
        requests.post(
            f"{settings.NEST_API_URL}/internal/resumes/failed",
            json={"resume_id": resume_id, "error": str(e)}
        )

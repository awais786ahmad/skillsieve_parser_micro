KEY_SKILLS = [
    "python", "django", "fastapi", "nestjs", "postgres",
    "redis", "docker", "aws", "react", "typescript"
]

def calculate_ats_score(text: str) -> dict:
    text_lower = text.lower()
    matched = [s for s in KEY_SKILLS if s in text_lower]

    score = int((len(matched) / len(KEY_SKILLS)) * 100)

    return {
        "score": score,
        "matched_skills": matched,
        "missing_skills": list(set(KEY_SKILLS) - set(matched))
    }

from pathlib import Path
import tempfile
import shutil

_TEMP_DIR = Path(tempfile.gettempdir()) / "skillsieve_parser_micro"

def ensure_temp_dir() -> Path:
    _TEMP_DIR.mkdir(parents=True, exist_ok=True)
    return _TEMP_DIR

def create_job_temp_dir(resume_id: str) -> Path:
    base = ensure_temp_dir()
    job_dir = base / resume_id
    job_dir.mkdir(parents=True, exist_ok=True)
    return job_dir

def cleanup_job_dir(resume_id: str):
    path = _TEMP_DIR / resume_id
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)

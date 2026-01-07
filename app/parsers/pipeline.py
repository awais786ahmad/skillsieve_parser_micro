from pathlib import Path

from app.parsers.downloader import download_file
from app.parsers.detector import detect_file_type
from app.core.temp_files import create_job_temp_dir
from app.core.logger import logger

async def prepare_file(
    resume_id: str,
    file_url: str,
) -> dict:
    job_dir = create_job_temp_dir(resume_id)

    file_path = job_dir / "resume"

    download_meta = await download_file(
        file_url,
        file_path,
    )

    detect_meta = detect_file_type(file_path)

    logger.info(
        f"[FILE_READY] resume_id={resume_id} type={detect_meta['type']}"
    )

    return {
        "path": file_path,
        "size": download_meta["size"],
        "sha256": download_meta["sha256"],
        "type": detect_meta["type"],
        "mime": detect_meta["mime"],
    }

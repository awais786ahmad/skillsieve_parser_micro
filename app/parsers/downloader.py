from pathlib import Path
import httpx
import hashlib

from app.core.logger import logger

async def download_file(
    url: str,
    dest: Path,
) -> dict:
    """
    Downloads file and returns metadata
    """
    logger.info(f"[DOWNLOAD] {url}")

    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.get(url)
        r.raise_for_status()
        dest.write_bytes(r.content)

    size = dest.stat().st_size
    sha256 = hashlib.sha256(dest.read_bytes()).hexdigest()

    logger.info(
        f"[DOWNLOADED] file={dest.name} size={size}"
    )

    return {
        "path": dest,
        "size": size,
        "sha256": sha256,
    }

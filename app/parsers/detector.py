from pathlib import Path
import magic

from app.core.logger import logger

class FileType:
    PDF = "pdf"
    DOCX = "docx"
    IMAGE_PDF = "image_pdf"
    UNKNOWN = "unknown"

def detect_file_type(file_path: Path) -> dict:
    mime = magic.from_file(str(file_path), mime=True)
    ext = file_path.suffix.lower()

    logger.info(
        f"[DETECT] ext={ext} mime={mime}"
    )

    if mime == "application/pdf":
        return {
            "type": FileType.PDF,
            "mime": mime,
        }

    if (
        mime
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        return {
            "type": FileType.DOCX,
            "mime": mime,
        }

    if mime.startswith("image/"):
        return {
            "type": FileType.IMAGE_PDF,
            "mime": mime,
        }

    return {
        "type": FileType.UNKNOWN,
        "mime": mime,
    }

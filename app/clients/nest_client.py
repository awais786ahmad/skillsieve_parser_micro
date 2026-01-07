import httpx
from app.config import settings
from app.core.logger import logger

async def update_resume_status(
    resume_id: str,
    status: str,
    payload: dict | None = None,
    error: str | None = None,
):
    url = f"{settings.NEST_CALLBACK_URL}/resumes/internal/status"

    logger.info(
        f"[CALLBACK] resume_id={resume_id} status={status}"
    )
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                url,
                params={  # ✅ QUERY STRING
                    "resume_id": resume_id,
                },
                headers={
                    "Authorization": f"Bearer {settings.NEST_INTERNAL_API_KEY.strip()}"
                },
                json={
                    "status": status,
                    "payload": payload,
                    "error": error,
                },
            )

        logger.info(
            f"[CALLBACK_SUCCESS] resume_id={resume_id} status_code={response}"
        )

    except Exception:
        logger.exception(
            f"[CALLBACK_FAILED] resume_id={resume_id}"
        )
        raise

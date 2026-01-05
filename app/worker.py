import asyncio
import json
import logging
import socket

from app.queues.redis_client import redis_client
from app.schemas.resume_job import ResumeJobPayload
from app.clients.nest_client import update_resume_status

STREAM_NAME = "resume-jobs"
GROUP_NAME = "resume-workers"
CONSUMER_NAME = socket.gethostname()

logging.basicConfig(level=logging.INFO)

# ---------- JOB PROCESSOR ----------

async def process_job(job_data: dict):
    payload = ResumeJobPayload(**job_data)

    logging.info(f"[PROCESSING] resume_id={payload.resume_id}")

    await update_resume_status(payload.resume_id, "processing")

    try:
        parsed_data = {
            "identity": {},
            "skills": [],
        }

        await update_resume_status(
            payload.resume_id,
            "parsed",
            payload=parsed_data
        )

        logging.info(f"[SUCCESS] resume_id={payload.resume_id}")

    except Exception as e:
        logging.exception("Parsing failed")

        await update_resume_status(
            payload.resume_id,
            "failed",
            error=str(e)
        )
        raise


# ---------- STREAM CONSUMER ----------

async def consume_stream():
    # Create consumer group (idempotent)
    try:
        await redis_client.xgroup_create(
            STREAM_NAME,
            GROUP_NAME,
            id="0",
            mkstream=True,
        )
    except Exception:
        pass  # already exists

    logging.info(
        f"Worker started | group={GROUP_NAME} consumer={CONSUMER_NAME}"
    )

    while True:
        messages = await redis_client.xreadgroup(
            GROUP_NAME,
            CONSUMER_NAME,
            streams={STREAM_NAME: ">"},
            count=1,
            block=5000,
        )

        for _, entries in messages:
            for message_id, data in entries:
                try:
                    payload = json.loads(data["payload"])
                    await process_job(payload)

                    await redis_client.xack(
                        STREAM_NAME,
                        GROUP_NAME,
                        message_id,
                    )

                except Exception:
                    logging.exception("Job failed")
                    # NO ACK → message can be retried


# ---------- ENTRYPOINT ----------

async def start_worker():
    await consume_stream()

if __name__ == "__main__":
    asyncio.run(start_worker())

import logging
import sys

def setup_logger():
    logger = logging.getLogger("resume_parser")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Prevent duplicate logs
    logger.propagate = False

    return logger


logger = setup_logger()

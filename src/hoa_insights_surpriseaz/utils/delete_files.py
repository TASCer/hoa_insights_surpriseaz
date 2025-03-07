import logging
import os

from logging import Logger
from pathlib import Path

logger: Logger = logging.getLogger(__name__)

MANAGEMENT_PDF_PATH = Path.cwd().parent / "output" / "pdf" / "MANAGEMENT.pdf"


def delete(file: Path = MANAGEMENT_PDF_PATH):
    if Path.exists(file):
        Path.unlink(file)
        logger.info("DOWNLOADED MANAGEMENT PDF FILE DELETED")

        return True

    else:
        logger.warning(f"** FILE: {file} NOT FOUND **")

        return False


if __name__ == "__main__":
    delete()

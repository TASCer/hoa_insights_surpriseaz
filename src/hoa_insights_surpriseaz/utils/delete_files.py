import logging

from logging import Logger
from pathlib import Path

logger: Logger = logging.getLogger(__name__)

MANAGEMENT_PDF_PATH = Path.cwd() / "output" / "pdf" / "MANAGEMENT.pdf"


def delete(file: Path = MANAGEMENT_PDF_PATH) -> bool:
    """
    Function deletes a file given.

    Args:
        file (Path, optional): file to delete. Defaults to MANAGEMENT_PDF_PATH.

    Returns:
        bool: True if successful
    """
    if Path.exists(file):
        Path.unlink(file)
        logger.info(f"DOWNLOADED COMMUNITY MANAGEMENT PDF {file.name} DELETED")

        return True

    else:
        logger.warning(f"** FILE: {file} NOT FOUND **")

        return False


if __name__ == "__main__":
    delete()

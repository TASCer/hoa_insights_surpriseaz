import logging
from logging import Logger
from pathlib import Path

logger: Logger = logging.getLogger(__name__)


def delete(file: Path) -> bool:
    """
    Function deletes a file with given path.

    Args:
        file (Path, optional): file to delete.

    Returns:
        bool: True if successful
    """
    if Path.exists(file):
        Path.unlink(file)
        logger.info(f"{file.name} DELETED")

        return True

    else:
        logger.warning(f"** FILE DELETION FAILED: {file} NOT FOUND **")

        return False

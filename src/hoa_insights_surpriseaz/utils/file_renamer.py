import logging

from logging import Logger
from pathlib import Path

logger: Logger = logging.getLogger(__name__)


def rename(old: Path, new: Path) -> bool:
    """
    Function renames files.

    Args:
        old (Path): file to be renamed
        new (Path): renamed file

    Returns:
        bool: True if successful
    """
    if old.exists():
        try:
            old.replace(new)
            logger.info(f"FILE: {old.name} renamed to: {new.name}")

            return True

        except FileNotFoundError as ffe:
            logger.error(ffe)

            return False

    else:
        return False

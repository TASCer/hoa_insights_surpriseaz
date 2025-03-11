import logging

from logging import Logger
from pathlib import Path

logger: Logger = logging.getLogger(__name__)


def rename(old: Path, new: Path) -> bool:
    if old:
        try:
            old.replace(new)
            logger.info(f"FILE: {old.name} renamed to: {new.name}")

            return True

        except FileNotFoundError as ffe:
            logger.error(ffe)

            return False


if __name__ == "__main__":
    rename()

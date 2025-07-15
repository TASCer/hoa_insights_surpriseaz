import logging

from logging import Logger
from pathlib import Path

logger: Logger = logging.getLogger(__name__)


def rename(old: Path, new: Path) -> bool:
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


if __name__ == "__main__":
    # ORIGINAL RENAME
    rename(
        old=Path(
            "/home/todd/python_projects/hoa_insights_surpriseaz/tests/input/TEST-ORIGINAL-PDF.pdf"
        ),
        new=Path(
            "/home/todd/python_projects/hoa_insights_surpriseaz/tests/input/TEST-RENAMED-PDF.pdf"
        ),
    )
    # PUT BACK
    # rename(
    #     old=Path(
    #         "/home/todd/python_projects/hoa_insights_surpriseaz/tests/input/TEST-RENAMED-PDF.pdf"
    #     ),
    #     new=Path(
    #         "/home/todd/python_projects/hoa_insights_surpriseaz/tests/input/TEST-ORIGINAL-PDF.pdf"
    #     ),
    # )

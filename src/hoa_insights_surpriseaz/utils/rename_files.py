import os
import logging
from logging import Logger

logger: Logger = logging.getLogger(__name__)

ORIG_PDF_FILEPATH: str = "../output/pdf/HOA Contact List (PDF).pdf"
ORIG_PDF_FILENAME: str = ORIG_PDF_FILEPATH.split("/")[-1]
NEW_PDF_FILEPATH: str = "../output/pdf/MANAGEMENT.pdf"
NEW_PDF_FILENAME: str = NEW_PDF_FILEPATH.split("/")[-1]

TEST_PDF_FILEPATH: str = "../output/pdf/StrengthLeadershipTest.pdf"
TEST_PDF_FILENAME: str = TEST_PDF_FILEPATH.split("/")[-1]
NEW_TEST_PDF_FILEPATH: str = "../output/pdf/Gallop.pdf"
NEW_TEST_PDF_FILENAME: str = NEW_TEST_PDF_FILEPATH.split("/")[-1]


def rename():
    if os.path.abspath(f"../output/pdf/{ORIG_PDF_FILEPATH}"):
        try:
            os.rename(ORIG_PDF_FILEPATH, NEW_PDF_FILEPATH)
            logger.info(f"Downloading Completed, renamed file to: {NEW_PDF_FILENAME}")
        except FileNotFoundError as ffe:
            logger.error(ffe)

    if os.path.abspath(f"../output/pdf/{TEST_PDF_FILEPATH}"):
        try:
            os.rename(TEST_PDF_FILEPATH, NEW_TEST_PDF_FILEPATH)
            logger.info(
                f"Downloading Completed, renamed file to: {NEW_TEST_PDF_FILENAME}"
            )
        except FileNotFoundError as ffe:
            logger.error(ffe)

    return True


if __name__ == "__main__":
    rename()

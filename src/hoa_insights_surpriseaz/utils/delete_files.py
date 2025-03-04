import logging
import os

from logging import Logger

logger: Logger = logging.getLogger(__name__)

MANAGEMENT_PDF_PATH = "./output/pdf/MANAGEMENT.pdf"


def delete():
    if os.path.exists(MANAGEMENT_PDF_PATH):
        os.remove(MANAGEMENT_PDF_PATH)
        logger.info("DOWNLOADED MANAGEMENT PDF FILE DELETED")

        return True

    else:
        logger.warning("**NO DOWNLOADED MANAGEMENT PDF FILE FOUND**")

        return False


if __name__ == "__main__":
    delete()

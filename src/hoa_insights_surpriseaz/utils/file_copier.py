import platform
import logging
import os
import shutil


from logging import Logger
from pathlib import Path
# from hoa_insights_surpriseaz import my_secrets

logger: Logger = logging.getLogger(__name__)

WEB_SERVER_REPORT_PATH_LINUX = Path("/var/www/html/hoa/reports/")
WEB_SERVER_REPORT_PATH_WINDOWS = Path(r"\\OPERATIONS\c$\inetpub\wwwroot\TASCSlocal\hoa\reports")


def copy(file: str) -> bool:
    if not platform.system() == "Windows":
        try:
            os.system(f"cp {file} {WEB_SERVER_REPORT_PATH_LINUX}")
            logger.info(f"{file.split('/')[-1]} sent to tascs.test web server")
        except BaseException as e:
            logger.critical(f"{file} NOT sent to tascs.test web server. {e}")
    else:
        try:
            shutil.copy(file, WEB_SERVER_REPORT_PATH_WINDOWS)

        except (IOError, FileNotFoundError) as e:
            logger.error(e)

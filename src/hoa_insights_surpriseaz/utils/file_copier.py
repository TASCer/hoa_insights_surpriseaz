import platform
import logging
import os
import shutil


from logging import Logger
from pathlib import Path
from hoa_insights_surpriseaz import my_secrets

logger: Logger = logging.getLogger(__name__)

# web_server_path_linux_local = "/var/www/html/hoa/reports/"
# web_server_path_linux_remote = "todd@debian:/var/www/html/hoa/reports/"
# web_server_path_windows = r"\\OPERATIONS\c$\inetpub\wwwroot\TASCSlocal\hoa\reports"

WEB_SERVER_REPORT_PATH = Path("/var/www/html/hoa/reports/")


def copy(file: str) -> bool:
    if not platform.system() == "Windows":
        try:
            os.system(f"cp {file} {WEB_SERVER_REPORT_PATH}")
            logger.info(f"{file.split('/')[-1]} sent to tascs.test web server")
        except BaseException as e:
            logger.critical(f"{file} NOT sent to tascs.test web server. {e}")
    else:
        try:
            shutil.copy(file, my_secrets.web_server_path_windows)

        except (IOError, FileNotFoundError) as e:
            logger.error(e)

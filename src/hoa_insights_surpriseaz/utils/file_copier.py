import platform
import logging
import os
import shutil


from logging import Logger
from hoa_insights_surpriseaz import my_secrets

logger: Logger = logging.getLogger(__name__)


def copy(file: str) -> bool:
    if not platform.system() == "Windows":
        try:
            os.system(f"cp {file} {my_secrets.web_server_path_linux_local}")
            logger.info(f"{file.split('/')[-1]} sent to tascs.test web server")
        except BaseException as e:
            logger.critical(f"{file} NOT sent to tascs.test web server. {e}")
    else:
        try:
            shutil.copy(file, my_secrets.web_server_path_windows)

        except (IOError, FileNotFoundError) as e:
            logger.error(e)

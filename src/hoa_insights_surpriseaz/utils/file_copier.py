import platform
import logging
import os
import shutil


from logging import Logger
from pathlib import Path

logger: Logger = logging.getLogger(__name__)

WEB_SERVER_REPORT_PATH_LINUX = Path("/var/www/html/hoa/reports/")
WEB_SERVER_REPORT_PATH_WINDOWS = Path(
    r"\\OPERATIONS\c$\inetpub\wwwroot\TASCSlocal\hoa\reports"
)


def to_webserver(to_copy: Path, copy_to: Path = WEB_SERVER_REPORT_PATH_LINUX) -> None:
    """
    Function copies files to webserver for integration with website.

    Args:
        to_copy (Path): source
        copy_to (Path, optional): destination. Defaults to WEB_SERVER_REPORT_PATH_LINUX.
    """
    if copy_to.exists() and to_copy.exists():
        if not platform.system() == "Windows":
            source = str(to_copy)
            destination = str(copy_to)
            try:
                os.system(f"cp {source} {destination}")
                logger.info(f"{to_copy.name} sent to tascs.test web server locally.")
            except BaseException as e:
                logger.critical(
                    f"{to_copy.name} NOT sent to tascs.test web server locally. {e}"
                )
        else:
            try:
                shutil.copy(to_copy, copy_to)

            except (IOError, FileNotFoundError) as e:
                logger.error(e)

    if not copy_to.exists() and to_copy.exists():
        copy_to = Path.cwd()
        if not platform.system() == "Windows":
            try:
                os.system(f"scp {to_copy} todd@debian.tascs.test:{copy_to}")
                logger.info(f"{to_copy.name} sent to tascs.test web server remotely")
            except BaseException as e:
                logger.critical(
                    f"{to_copy} NOT sent to tascs.test web server remotely. {e}"
                )
        elif platform.system() == "Windows":
            try:
                shutil.copy(to_copy, copy_to)

            except (IOError, FileNotFoundError) as e:
                logger.error(e)

    if copy_to.exists() and not to_copy.exists():
        logger.warning(f"{to_copy} file does not exist")

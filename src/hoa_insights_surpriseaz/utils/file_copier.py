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
    if copy_to.exists():
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

    else:
        # copy_to = Path("/home/todd/hoa/reports/").absolute()
        print(copy_to, type(copy_to))
        if not platform.system() == "Windows":
            try:
                os.system(f"scp {to_copy} todd@debian.tascs.test:{copy_to}")
                logger.info(f"{to_copy.name} sent to tascs.test web server remotely")
            except BaseException as e:
                logger.critical(
                    f"{to_copy} NOT sent to tascs.test web server remotely. {e}"
                )
        else:
            try:
                os.system(f"scp {to_copy} todd@debian.tascs.test:{copy_to}")

            except (IOError, FileNotFoundError) as e:
                logger.error(e)


def to_folder(source: Path, destination: Path) -> None:
    pass
    # if not platform.system() == "Windows":
    #     try:
    #         os.system(f"cp {file} {WEB_SERVER_REPORT_PATH_LINUX}")
    #         logger.info(f"{file.split('/')[-1]} sent to tascs.test web server")
    #     except BaseException as e:
    #         logger.critical(f"{file} NOT sent to tascs.test web server. {e}")
    # else:
    #     try:
    #         shutil.copy(file, WEB_SERVER_REPORT_PATH_WINDOWS)

    #     except (IOError, FileNotFoundError) as e:
    #         logger.error(e)

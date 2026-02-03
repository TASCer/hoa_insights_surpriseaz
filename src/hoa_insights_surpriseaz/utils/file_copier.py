from enum import Enum
import platform
import logging
import os
import shutil

from logging import Logger
from pathlib import Path

logger: Logger = logging.getLogger(__name__)


def linux_server(source, destination, source_check, destination_check) -> None:
    """
    Function copies files for Linux systems
    """
    if source_check and destination_check:
        try:
            os.system(f"cp {source} {destination}")
            logger.info(f"'{source.name}' sent to 'tascs.test' web server")
        except BaseException as e:
            logger.critical(f"'{source.name}' NOT sent to 'tascs.test' web server {e}")

    if not destination_check and source_check:
        copy_to = Path("~")
        try:
            os.system(f"scp {source} todd@debian.tascs.test:{copy_to}")
            logger.info(f"'{source.name}' sent to tascs.test web server remotely")
        except BaseException as e:
            logger.critical(f"{source} NOT sent to tascs.test web server remotely. {e}")


def windows_server(source, destination) -> None:
    """
    Function copies files for Windows systems
    """

    try:
        shutil.copy(source, destination)

    except (IOError, FileNotFoundError) as e:
        logger.error(e)


def to_webserver(to_copy: Path, webserver: Enum) -> None:
    """
    Function copies files to webserver 'reports' directory based on server OS.

    Args:
        to_copy (Path): source
        copy_to (Path, optional): destination. Defaults to WEB_SERVER_REPORT_PATH_LINUX.
    """
    source_check = to_copy.exists()
    destination_check = webserver.value.exists()
    client_system = platform.system()

    if not source_check:
        logger.warning(f"SOURCE: '{to_copy}' file does not exist")
        raise FileNotFoundError(f"SOURCE: '{to_copy}' file does not exist")

    if client_system == "Linux":
        linux_server(to_copy, webserver.value, source_check, destination_check)

    if client_system == "Windows" and all([source_check, destination_check]):
        windows_server(to_copy, webserver.value)


if __name__ == "__main__":
    from hoa_insights_surpriseaz.main import WEB_SERVER

    webserver = WEB_SERVER
    to_webserver(
        to_copy=Path.cwd().parent
        / "output"
        / "web_reports"
        / "parcel_changes"
        / "recent_changes.html",
        webserver=webserver,
    )

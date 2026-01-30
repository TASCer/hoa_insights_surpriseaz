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


def windows_server(source, destination, source_check, destination_check) -> None:
    """
    Function copies files for Windows systems
    """
    if source_check and destination_check:
        try:
            shutil.copy(source, destination)

        except (IOError, FileNotFoundError) as e:
            logger.error(e)


def to_webserver(to_copy: Path, copy_to: Path = WEB_SERVER_REPORT_PATH_LINUX) -> None:
    """
    Function copies files to webserver for integration with website.

    Args:
        to_copy (Path): source
        copy_to (Path, optional): destination. Defaults to WEB_SERVER_REPORT_PATH_LINUX.
    """
    source_check = to_copy.exists()
    destination_check = copy_to.exists()
    system = platform.system()

    if not source_check:
        logger.warning(f"SOURCE: '{to_copy}' file does not exist")
        raise FileNotFoundError(f"SOURCE: '{to_copy}' file does not exist")

    if system == "Linux":
        linux_server(to_copy, copy_to, source_check, destination_check)

    if system == "Windows":
        windows_server(to_copy, copy_to, source_check, destination_check)


if __name__ == "__main__":
    to_webserver(
        Path.cwd().parent
        / "output"
        / "web_reports/parcel_changes"
        / "recent_changes.html"
    )

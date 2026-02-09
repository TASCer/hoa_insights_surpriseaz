from enum import Enum
import platform
import logging
import os
import shutil
import socket

from hoa_insights_surpriseaz import my_secrets
from logging import Logger
from pathlib import Path

logger: Logger = logging.getLogger(__name__)


def linux_server(source, destination, secure_copy_needed, webserver_fqdn) -> None:
    """
    Function copies files for Linux systems
    """
    if not secure_copy_needed:
        try:
            os.system(f"cp {source} {destination}")
            logger.info(f"'{source.name}' sent to '{webserver_fqdn}' web server")
        except BaseException as e:
            logger.critical(
                f"'{source.name}' NOT sent to '{webserver_fqdn}' web server {e}"
            )

    else:
        try:
            os.system(f"scp {source} todd@{webserver_fqdn}:{destination}")
            logger.info(
                f"'{source.name}' sent to '{webserver_fqdn}' web server securely"
            )
        except BaseException as e:
            logger.critical(
                f"{source} NOT sent to {webserver_fqdn} web server securely. {e}"
            )


def windows_server(source, destination, secure_copy_needed, webserver_fqdn) -> None:
    """
    Function copies files for Windows systems
    """
    if not secure_copy_needed:
        try:
            shutil.copy(source, destination)

        except (IOError, FileNotFoundError) as e:
            logger.error(e)

    else:
        try:
            os.system(f"scp {source} todd@'{webserver_fqdn}':{destination}")
        except Exception as e:
            print(e)


def to_webserver(to_copy: Path, webserver: Enum) -> None:
    """
    Function copies files to webserver 'reports' directory based on server OS.

    Args:
        to_copy (Path): source
        copy_to (Path, optional): destination. Defaults to WEB_SERVER_REPORT_PATH_LINUX.
    """
    client_system = platform.system()
    client_fqdn: str = socket.getfqdn()

    webserver_system = webserver.name
    webserver_fqdn: str = my_secrets.prod_local_dbhost

    secure_copy_needed: bool = webserver_fqdn != client_fqdn

    if webserver.name == "LINUX":
        linux_server(
            source=to_copy,
            destination=webserver.value,
            secure_copy_needed=secure_copy_needed,
            webserver_fqdn=webserver_fqdn,
        )

    if webserver.name == "WINDOWS":
        windows_server(
            source=to_copy,
            destination=webserver.value,
            secure_copy_needed=secure_copy_needed,
            webserver_fqdn=webserver_fqdn,
        )


if __name__ == "__main__":
    from hoa_insights_surpriseaz.main import WebServer

    webserver = WebServer.LINUX
    print(webserver, webserver.name, webserver.value)
    to_webserver(
        to_copy=Path.cwd().parent
        / "output"
        / "web_reports"
        / "parcel_changes"
        / "recent_changes.html",
        webserver=webserver,
    )

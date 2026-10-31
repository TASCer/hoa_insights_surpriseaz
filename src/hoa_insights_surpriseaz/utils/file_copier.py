import logging
import os
import platform
import shutil
import socket
import subprocess
import sys
from enum import Enum
from logging import Logger
from pathlib import Path

from dotenv import load_dotenv

from hoa_insights_surpriseaz.utils import ssh_agent_check

load_dotenv()

logger: Logger = logging.getLogger(__name__)


def linux_server(
    source: Path,
    destination: Path,
    secure_copy_needed: bool,
    webserver_fqdn: str,
    client_system: str,
) -> None:
    """
    Function copies files to Linux systems

    :param source: path of file to copy
    :param destination: path of copy to location
    :param secure_copy_needed: True if webserver remote
    :param webserver_fqdn: webserver full dns name
    :param client_system: client OS
    """
    if not secure_copy_needed:
        try:
            result = subprocess.run(["cp", f"{source}", f"{destination}"], check=True)
            if result.returncode == 0:
                logger.info(f"'{source.name}' sent to '{webserver_fqdn}' web server")
        except FileNotFoundError as e:
            logger.critical(
                f"'{source.name}' NOT sent to '{webserver_fqdn}' web server {e}"
            )

    else:
        if not ssh_agent_check.is_ssh_agent_running_env():
            logger.error("FILES CANNOT BE SENT.")

        else:
            try:
                result = subprocess.run(
                    [
                        "scp",
                        f"{source}",
                        f"{os.environ['WEBSERVER_USER']}@{webserver_fqdn}:{destination}",
                    ],
                    check=True,
                )
                if result.returncode == 0:
                    logger.info(
                        f"'{source.name}' sent to '{webserver_fqdn}' web server securely"
                    )
            except FileNotFoundError as e:
                logger.critical(
                    f"{source.name} NOT sent to {webserver_fqdn} web server securely. {e}"
                )


def windows_server(
    source: Path,
    destination: Path,
    secure_copy_needed: bool,
    webserver_fqdn: str,
    client_system: str,
) -> None:
    """
    Function copies files to Windows systems

    :param source: path of file to copy
    :param destination: path of copy to location
    :param secure_copy_needed: True if webserver remote
    :param webserver_fqdn: webserver full dns name
    :param client_system: client OS
    """
    if not secure_copy_needed:
        try:
            shutil.copy(source, destination)
            logger.info(f"'{source.name}' sent to '{webserver_fqdn}' web server")

        except (OSError, FileNotFoundError) as e:
            logger.error(e)

    else:
        try:
            result = subprocess.run(
                [
                    "scp",
                    f"{source}",
                    f"{os.environ['WEBSERVER_USER']}@{webserver_fqdn}:{destination}",
                ],
                check=True,
            )
            if result.returncode == 0:
                logger.info(f"'{source.name}' sent to '{webserver_fqdn}' web server")

        except (OSError, FileNotFoundError) as e:
            print(e)
            sys.exit()


def to_webserver(to_copy: Path, webserver: Enum) -> None:
    """
    Function sets up file copy to webserver 'reports' directory based on server OS.

    Args:
        to_copy (Path): source
        webserver: configured webserver destination
    """

    client_system = platform.system()
    client_fqdn: str = socket.getfqdn()

    webserver_fqdn: str = os.environ["DEVELOPMENT"]

    secure_copy_needed: bool = webserver_fqdn != client_fqdn

    if webserver.name == "LINUX":
        linux_server(
            source=to_copy,
            destination=webserver.value,
            secure_copy_needed=secure_copy_needed,
            webserver_fqdn=webserver_fqdn,
            client_system=client_system,
        )

    if webserver.name == "WINDOWS":
        windows_server(
            source=to_copy,
            destination=webserver.value,
            secure_copy_needed=secure_copy_needed,
            webserver_fqdn=webserver_fqdn,
            client_system=client_system,
        )

    if webserver.name == "TESTING":
        windows_server(
            source=to_copy,
            destination=webserver.value,
            secure_copy_needed=False,
            webserver_fqdn=webserver_fqdn,
            client_system=client_system,
        )


if __name__ == "__main__":
    from hoa_insights_surpriseaz.main import WebServer

    webserver = WebServer.LINUX
    print(webserver, webserver.name, webserver.value)
    to_webserver(
        to_copy=Path.cwd().parent
        / "output"
        / "web_reports"
        / "financial"
        / "community_ytd_sales_avg.html",
        webserver=webserver,
    )

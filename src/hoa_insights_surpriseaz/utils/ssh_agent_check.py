import logging
import os
from logging import Logger

# from venv import logger

logger: Logger = logging.getLogger(__name__)


def is_ssh_agent_running_env() -> bool:
    """
    Function checks if SSH Agent is running by inspecting environment variables.

    :return: True if running
    """
    if "SSH_AUTH_SOCK" in os.environ:
        print(
            f"SSH agent appears to be running. SSH_AUTH_SOCK: {os.environ['SSH_AUTH_SOCK']}"
        )
        logger.info(
            f"SSH agent appears to be running. SSH_AUTH_SOCK: {os.environ['SSH_AUTH_SOCK']}"
        )

        return True
    else:
        print(
            "SSH_AUTH_SOCK environment variable not found. SSH agent might not be running or configured for this session."
        )
        logger.error(
            "SSH_AUTH_SOCK environment variable not found. SSH agent might not be running or configured for this session."
        )

        return False

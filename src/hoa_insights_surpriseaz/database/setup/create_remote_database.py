import logging

from hoa_insights_surpriseaz.database import check_remote_database, models_remote
from logging import Logger
from sqlalchemy import Engine

logger: Logger = logging.getLogger(__name__)


def create(remote_engine: Engine) -> bool:
    """
    Function creates remote database
    """
    logger.info(f"CREATING DB ON: {remote_engine.url.host}")

    if check_remote_database.schema(engine=remote_engine):
        models_remote.Base.metadata.create_all(remote_engine)
        logger.info(f"CREATED DB ON: {remote_engine.url.host}")
        return True
    else:
        return False

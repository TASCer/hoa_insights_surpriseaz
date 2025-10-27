import logging

from hoa_insights_surpriseaz.database import check_remote_database, models_remote
from hoa_insights_surpriseaz.database.setup import populate_remote_tables
from logging import Logger
from sqlalchemy import Engine
from sqlalchemy.orm import Session

logger: Logger = logging.getLogger(__name__)


def create(remote_engine: Engine) -> None:
    """
    Function creates remote database
    """ 
    logger.info(f"* CREATING DB ON: {remote_engine.url.host} *")

    if check_remote_database.schema(engine=remote_engine):
        models_remote.Base.metadata.create_all(remote_engine)
        logger.info(f"- CREATED DB ON: {remote_engine.url.host} -")
        return True

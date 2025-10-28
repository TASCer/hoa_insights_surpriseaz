import logging

from hoa_insights_surpriseaz.database import models_remote
from logging import Logger
from sqlalchemy import Engine, exc
from sqlalchemy_utils import database_exists, create_database

logger: Logger = logging.getLogger(__name__)


def create(remote_engine: Engine) -> bool:
    """
    _summary_

    :param remote_engine: _description_
    :return: _description_
    """    
    logger.info(f"CREATING DB ON: {remote_engine.url.host}")

    try:
        if not database_exists(remote_engine.url):
            create_database(remote_engine.url)

    except (exc.SQLAlchemyError, exc.OperationalError) as e:
        logger.critical(str(e))

        return False

    models_remote.Base.metadata.create_all(remote_engine)
    logger.info(f"CREATED DB ON: {remote_engine.url.host}")

    return True

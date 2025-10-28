import logging

from hoa_insights_surpriseaz.database import models_local
from hoa_insights_surpriseaz.database.setup import (
    create_local_triggers,
    create_local_views,
    create_local_procs,
)

from logging import Logger
from sqlalchemy import Engine, exc
from sqlalchemy_utils import database_exists, create_database

logger: Logger = logging.getLogger(__name__)


def create(engine: Engine) -> bool:
    """
    _summary_

    :param engine: _description_
    :return: _description_
    """    

    logger.info(f"CREATNG DB ON: {engine.url.host}")
    try:
        if not database_exists(engine.url):
            create_database(engine.url)

    except (exc.SQLAlchemyError, exc.OperationalError) as e:
        logger.critical(str(e))
        return False

    models_local.Base.metadata.create_all(engine)
    triggers: bool = create_local_triggers.all(engine)
    views: bool = create_local_views.all(engine)
    stored_proc: bool = create_local_procs.all(engine)
    if all((triggers, views, stored_proc)):
        logger.info(f"CREATED DB ON: {engine.url.host}")
        return True

    else:
        return False

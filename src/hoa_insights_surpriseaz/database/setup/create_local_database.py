import logging

from hoa_insights_surpriseaz.database import check_local_database, models_local

from logging import Logger
from sqlalchemy import Engine

logger: Logger = logging.getLogger(__name__)


def create(engine: Engine) -> bool:
    """
    Function creates a db engine and checks if schema, table, triggers, views are created.
    Returns a list of community totals for remote table population.
    """

    logger.info(f"CREATNG DB ON: {engine.url.host}")
    if check_local_database.schema(engine):
        models_local.Base.metadata.create_all(engine)
    triggers: bool = check_local_database.triggers(engine)
    views: bool = check_local_database.views(engine)
    stored_proc: bool = check_local_database.stored_procs(engine)
    if all((triggers, views, stored_proc)):
        logger.info(f"CREATED DB ON: {engine.url.host}")
        return True

    else:
        return False

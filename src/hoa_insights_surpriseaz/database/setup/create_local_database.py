import logging

from hoa_insights_surpriseaz.database import check_local_database, models_local
from hoa_insights_surpriseaz.database.setup import populate_local_tables
from logging import Logger
from sqlalchemy import Engine
from sqlalchemy.orm import Session

logger: Logger = logging.getLogger(__name__)


def create(engine: Engine, session: Session) -> tuple[list, Session]:
    """
    Function creates a db engine and checks if schema, table, triggers, views are created.
    Returns a list of community totals for remote table population.
    """

    logger.info(f"*** STARTED LOCAL DATABASE SETUP ON: {engine.url.host} ***")
    if check_local_database.schema(engine):
        models_local.Base.metadata.create_all(engine)

        logger.info(
            f"\tLOCAL triggers created: {check_local_database.triggers(engine)}"
        )
        logger.info(f"\tLOCAL views created: {check_local_database.views(engine)}")
        logger.info(
            f"\tLOCAL stored proc(s) created: {check_local_database.stored_procs(engine)}"
        )
        logger.info(f"--- COMPLETED LOCAL DATABASE SETUP ON: {engine.url.host} ---")

        logger.info(f"*** STARTED LOCAL DATABASE POPULATION ON: {engine.url.host} ***")

        logger.info(
            f"\tLOCAL parcels table populated: {populate_local_tables.parcels(session)}"
        )
        community_totals = populate_local_tables.communities(session)
        logger.info(f"\tLOCAL communities table populated: {len(community_totals) > 0}")
        logger.info(
            f"--- COMPLETED LOCAL DATABASE POPULATION OF: {engine.url.database} ---"
        )

        return community_totals, session

    else:
        return [], session

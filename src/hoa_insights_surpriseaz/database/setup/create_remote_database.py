import logging

from hoa_insights_surpriseaz.database import check_remote_database, models_remote
from hoa_insights_surpriseaz.database.setup import populate_remote_tables
from logging import Logger
from sqlalchemy import Engine
from sqlalchemy.orm import Session

logger: Logger = logging.getLogger(__name__)


def create(
    community_totals: list[str], remote_engine: Engine, local_db: Session
) -> None:
    """
    Function creates remote DBMS and populates community_managers and communities tables with seed data.
    """
    logger.info(f"*** STARTED REMOTE DATABASE SETUP ON: {remote_engine.url.host} ***")

    remote_db = Session(remote_engine)

    if check_remote_database.schema(engine=remote_engine):
        models_remote.Base.metadata.create_all(remote_engine)

        logger.info(
            f"--- COMPLETED REMOTE DATABASE SETUP ON: {remote_engine.url.host} ---"
        )
        logger.info(
            f"*** STARTED REMOTE DATABASE POPULATION OF: {remote_engine.url.database} ***"
        )
        logger.info(
            f"\tREMOTE tables populated: {populate_remote_tables.communities(community_totals=community_totals, local_db=local_db, remote_db=remote_db)}"
        )
        logger.info(
            f"--- COMPLETED REMOTE DATABASE POPULATION OF: {remote_engine.url.database} ---"
        )

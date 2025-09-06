import logging

from hoa_insights_surpriseaz.database import (
    check_local_rdbms,
    check_remote_rdbms,
    models_local,
    models_remote,
)
from hoa_insights_surpriseaz.database.setup import (
    populate_local_tables,
    populate_remote_tables,
)
from logging import Logger, Formatter
from sqlalchemy import Engine
from sqlalchemy.orm import Session

root_logger: Logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

fh = logging.FileHandler("__database-setup__.log")
fh.setLevel(logging.DEBUG)

formatter: Formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s"
)
fh.setFormatter(formatter)

root_logger.addHandler(fh)

logger: Logger = logging.getLogger(__name__)


def create_local_dbms(engine: Engine, session: Session) -> tuple[list, Session | None]:
    """
    Function creates a db engine and checks if schema, table, triggers, views are created.
    Returns a list of community totals for remote table population.
    """

    logger.info(f"*** STARTED LOCAL DATABASE SETUP ON: {engine.url.host} ***")
    if check_local_rdbms.schema(engine):
        models_local.Base.metadata.create_all(engine)

        logger.info(f"\tLOCAL triggers created: {check_local_rdbms.triggers(engine)}")
        logger.info(f"\tLOCAL views created: {check_local_rdbms.views(engine)}")
        logger.info(
            f"\tLOCAL stored proc(s) created: {check_local_rdbms.stored_procs(engine)}"
        )
        logger.info(f"--- COMPLETED LOCAL DATABASE SETUP ON: {engine.url.host} ---")

        logger.info(f"*** STARTED LOCAL DATABASE POPULATION ON: {engine.url.host} ***")

        logger.info(
            f"\tLOCAL parcels table populated: {populate_local_tables.parcels(session)}"
        )
        community_totals = populate_local_tables.communities(session)
        logger.info(f"\tLOCAL communities table populated: {len(community_totals) > 0}")
        logger.info(
            f"--- COMPLETED LOCAL DATABASE POPULATION ON: {engine.url.database} ---"
        )

        return community_totals, session

    else:
        return None


def remote_database(
    community_totals: list[str], remote_engine: Engine, local_db_session: Session
) -> None:
    """
    Function creates remote DBMS and populates community_managers and communities tables with seed data.
    """
    logger.info(f"*** STARTED REMOTE DATABASE SETUP ON: {remote_engine.url.host} ***")

    remote_session = Session(remote_engine)

    if check_remote_rdbms.schema(engine=remote_engine):
        models_remote.Base.metadata.create_all(remote_engine)

        logger.info(
            f"--- COMPLETED REMOTE DATABASE SETUP ON: {remote_engine.url.host} ---"
        )
        logger.info(
            f"*** STARTED REMOTE DATABASE POPULATION ON: {remote_engine.url.database} ***"
        )
        logger.info(
            f"\tREMOTE tables populated: {populate_remote_tables.communities(community_totals, local_db_session, remote_db_session=remote_session)}"
        )
        logger.info(
            f"--- COMPLETED REMOTE DATABASE POPULATION ON: {remote_engine.url.database} ---"
        )


if __name__ == "__main__":
    community_management = create_local_dbms()
    remote_database(community_management)
    logger.info("********  DATABASE INITIALIZATION COMPLETE********")

import logging

from hoa_insights_surpriseaz.database import (
    check_local_rdbms,
    check_remote_rdbms,
    models_local,
    models_remote,
)
from hoa_insights_surpriseaz import my_secrets
from hoa_insights_surpriseaz.database.setup import (
    populate_local_tables,
    populate_remote_tables,
)
from logging import Logger, Formatter
from sqlalchemy import Engine, create_engine
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


def create_local_database(engine: Engine, session: Session) -> tuple[list, Session]:
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
            f"--- COMPLETED LOCAL DATABASE POPULATION OF: {engine.url.database} ---"
        )

        return community_totals, session

    else:
        return [], session


def create_remote_database(
    community_totals: list[str], remote_engine: Engine, local_db: Session
) -> None:
    """
    Function creates remote DBMS and populates community_managers and communities tables with seed data.
    """
    logger.info(f"*** STARTED REMOTE DATABASE SETUP ON: {remote_engine.url.host} ***")

    remote_db = Session(remote_engine)

    if check_remote_rdbms.schema(engine=remote_engine):
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


if __name__ == "__main__":
    LOCAL_DB_URI: str = f"{my_secrets.prod_debian_uri}"
    REMOTE_DB_URI: str = f"{my_secrets.prod_bluehost_uri}"

    LOCAL_ENGINE: Engine = create_engine(f"mysql+pymysql://{LOCAL_DB_URI}", echo=False)
    REMOTE_ENGINE: Engine = create_engine(
        f"mysql+pymysql://{REMOTE_DB_URI}", echo=False
    )

    local_session = Session(LOCAL_ENGINE)

    community_totals, local_db = create_local_database(
        engine=LOCAL_ENGINE, session=local_session
    )

    remote_session = Session(REMOTE_ENGINE)

    create_remote_database(
        community_totals=community_totals,
        remote_engine=REMOTE_ENGINE,
        local_db=local_session,
    )

    logger.info(
        f"DATABASES: {LOCAL_ENGINE.url.database}, {REMOTE_ENGINE.url.database} INITIALIZED."
    )

import logging

from hoa_insights_surpriseaz import my_secrets
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
from sqlalchemy import create_engine, Engine

root_logger: Logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

fh = logging.FileHandler("__database-setup__.log")
fh.setLevel(logging.DEBUG)

formatter: Formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s"
)
fh.setFormatter(formatter)

root_logger.addHandler(fh)

LOCAL_DB_URI: str = f"{my_secrets.prod_debian_uri}"
REMOTE_DB_URI: str = f"{my_secrets.test_bluehost_uri}"

LOCAL_DB_HOSTNAME: str = f"{my_secrets.prod_debian_dbhost}"
REMOTE_DB_HOSTNAME: str = f"{my_secrets.test_bluehost_dbhost}"

logger: Logger = logging.getLogger(__name__)


def local_database() -> list:
    engine: Engine = create_engine(f"mysql+pymysql://{LOCAL_DB_URI}", echo=False)

    logger.info(f"*** STARTED LOCAL DATABASE SETUP ON: {LOCAL_DB_HOSTNAME} ***")
    if check_local_rdbms.schema():
        models_local.Base.metadata.create_all(engine)

        logger.info(f"\tLOCAL triggers created: {check_local_rdbms.triggers()}")
        logger.info(f"\tLOCAL views created: {check_local_rdbms.views()}")
        logger.info(
            f"\tLOCAL stored proc(s) created: {check_local_rdbms.stored_procs()}"
        )
        logger.info(f"--- COMPLETED LOCAL DATABASE SETUP ON: {LOCAL_DB_HOSTNAME} ---")

        logger.info(
            f"*** STARTED LOCAL DATABASE POPULATION ON: {LOCAL_DB_HOSTNAME} ***"
        )
        logger.info(
            f"\tLOCAL parcels table populated: {populate_local_tables.parcels()}"
        )
        community_data_for_bluehost = populate_local_tables.communities()
        logger.info(
            f"\tLOCAL communities table populated: {len(community_data_for_bluehost) > 0}"
        )
        logger.info(
            f"--- COMPLETED LOCAL DATABASE POPULATION ON: {LOCAL_DB_HOSTNAME} ---"
        )

        return community_data_for_bluehost


def remote_database(management) -> None:
    engine: Engine = create_engine(f"mysql+pymysql://{REMOTE_DB_URI}", echo=False)

    logger.info(f"*** STARTED REMOTE DATABASE SETUP ON: {REMOTE_DB_HOSTNAME} ***")

    if check_remote_rdbms.schema():
        models_remote.Base.metadata.create_all(engine)

        logger.info(f"--- COMPLETED REMOTE DATABASE SETUP ON: {REMOTE_DB_HOSTNAME} ---")
        logger.info(
            f"*** STARTED REMOTE DATABASE POPULATION ON: {REMOTE_DB_HOSTNAME} ***"
        )
        logger.info(
            f"\tREMOTE tables populated: {populate_remote_tables.communities(management)}"
        )
        logger.info(
            f"--- COMPLETED REMOTE DATABASE POPULATION ON: {REMOTE_DB_HOSTNAME} ---"
        )


if __name__ == "__main__":
    community_management = local_database()
    remote_database(community_management)

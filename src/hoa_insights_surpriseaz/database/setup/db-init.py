import logging

from hoa_insights_surpriseaz import my_secrets

from hoa_insights_surpriseaz.database.setup import (
    create_local_database,
    create_remote_database,
    populate_local_tables,
    populate_remote_tables,
)
from logging import Logger, Formatter
from pathlib import Path
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

root_logger: Logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

DB_INIT_LOG_NAME = "__database-setup__.log"
MANAGEMENT_SEED_FILE: Path = Path.cwd() / "seed_data" / "surpriseaz-hoa-management.csv"
PARCELS_SEED_FILE: Path = Path.cwd() / "seed_data" / "parcel_constants.csv"


fh = logging.FileHandler(DB_INIT_LOG_NAME)
fh.setLevel(logging.DEBUG)

formatter: Formatter = logging.Formatter(
    "%(asctime)s - %(module)s - %(lineno)d - %(message)s"
)
fh.setFormatter(formatter)

root_logger.addHandler(fh)

logger: Logger = logging.getLogger(__name__)

LOCAL_DB_URI: str = f"{my_secrets.prod_local_uri}"
REMOTE_DB_URI: str = f"{my_secrets.prod_remote_uri}"
LOCAL_ENGINE: Engine = create_engine(f"mysql+pymysql://{LOCAL_DB_URI}", echo=False)
REMOTE_ENGINE: Engine = create_engine(f"mysql+pymysql://{REMOTE_DB_URI}", echo=False)


def local_database(
    local_engine=LOCAL_ENGINE,
    management_file=MANAGEMENT_SEED_FILE,
    parcel_file=PARCELS_SEED_FILE,
) -> None:
    """
    Function checks if local database has been created and populates table(s) if so.

    :param local_engine: database engine, defaults to LOCAL_ENGINE
    """
    local_session = Session(local_engine)

    local_database_created: bool = create_local_database.create(engine=local_engine)
    if local_database_created:
        logger.info(
            f"STARTED 'LOCAL' DATABASE POPULATION ON: '{local_engine.url.database}'"
        )
        populate_local_tables.parcels(db=local_session, parcel_file=parcel_file)
        populate_local_tables.communities(db=local_session)
        populate_local_tables.community_management(
            db=local_session, management_file=management_file
        )
        logger.info(
            f"COMPLETED 'LOCAL' DATABASE POPULATION ON: '{local_engine.url.database}'"
        )


def remote_database(remote_db=REMOTE_ENGINE, local_db=LOCAL_ENGINE) -> None:
    """
    Function checks if renote database has been created and populates table(s) if so.

    :param local_engine: database engine, defaults to REMOTE_ENGINE
    """
    remote_session = Session(remote_db)
    local_session = Session(local_db)
    remote_database_created: bool = create_remote_database.create(
        remote_engine=remote_db
    )

    if remote_database_created:
        logger.info(
            f"STARTED 'REMOTE' DATABASE POPULATION ON: '{remote_db.url.database}'"
        )

        populate_remote_tables.communities(remote_db=remote_session)

        populate_remote_tables.community_management(
            remote_db=remote_session, local_db=local_session
        )

        logger.info(
            f"COMPLETED 'REMOTE' DATABASE POPULATION ON: '{remote_db.url.database}'"
        )

    logger.info(
        f"DATABASES: ['{LOCAL_ENGINE.url.database}', '{REMOTE_ENGINE.url.database}'] INITIALIZED."
    )


def initialize() -> None:
    local_database()
    remote_database()


if __name__ == "__main__":
    print(f""" "{DB_INIT_LOG_NAME}" created.""")
    initialize()

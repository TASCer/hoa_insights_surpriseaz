import logging

from hoa_insights_surpriseaz import my_secrets
from hoa_insights_surpriseaz.database.setup import (
    create_local_database,
    create_remote_database,
    populate_local_tables,
    populate_remote_tables
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

LOCAL_DB_URI: str = f"{my_secrets.prod_local_uri}"
REMOTE_DB_URI: str = f"{my_secrets.prod_remote_uri}"
LOCAL_ENGINE: Engine = create_engine(f"mysql+pymysql://{LOCAL_DB_URI}", echo=False)
REMOTE_ENGINE: Engine = create_engine(f"mysql+pymysql://{REMOTE_DB_URI}", echo=False)


def main(local_engine=LOCAL_ENGINE, remote_engine=REMOTE_ENGINE):
    local_session = Session(local_engine)

    local_database_created = create_local_database.create(
        engine=local_engine, session=local_session
    )
    if local_database_created:
        populate_local_tables.parcels(local_session)
        community_instances = populate_local_tables.communities(local_session)
        logger.info(f"\t{len(community_instances)=}")
        logger.info(
            f"- COMPLETED POPULATION ON: {local_engine.url.database} -"
        )

    remote_session = Session(remote_engine)

    remote_database_created = create_remote_database.create(
        remote_engine=remote_engine)
        
    if remote_database_created:
        community_managers = populate_remote_tables.communities(remote_db=remote_session)
        populate_remote_tables.community_management(community_management_items=community_managers, remote_session=remote_session)

            
        logger.info(
            f"--- COMPLETED REMOTE DATABASE POPULATION OF: {remote_engine.url.database} ---"
        )

    logger.info(
        f"DATABASES: {LOCAL_ENGINE.url.database}, {REMOTE_ENGINE.url.database} INITIALIZED."
    )


if __name__ == "__main__":
    main()

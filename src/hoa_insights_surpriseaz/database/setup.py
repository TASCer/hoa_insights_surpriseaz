import logging

from logging import Logger, Formatter
from sqlalchemy import create_engine
from hoa_insights_surpriseaz import my_secrets
from hoa_insights_surpriseaz.database import (
    check_local_rdbms,
    check_remote_rdbms,
    models,
    populate_local_tables,
)
from hoa_insights_surpriseaz.database import (
    populate_remote_tables,
)

root_logger: Logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

fh = logging.FileHandler("__rdbms-creation__.log")
fh.setLevel(logging.DEBUG)

formatter: Formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s"
)
fh.setFormatter(formatter)

root_logger.addHandler(fh)

LOCAL_DB_URI = f"{my_secrets.prod_debian_uri}"
REMOTE_DB_HOSTNAME = f"{my_secrets.prod_bluehost_dbhost}"


logger: Logger = logging.getLogger(__name__)

engine = create_engine(f"mysql+pymysql://{LOCAL_DB_URI}", echo=False)


def create_local_tables() -> bool:
    if check_local_rdbms.schema():
        models.Base.metadata.create_all(engine)
        return True

    else:
        return False


if __name__ == "__main__":
    # CREATE LOCAL
    logger.info(
        f"*** STARTED LOCAL DATABASE SETUP ON: {my_secrets.prod_debian_dbhost} ***"
    )
    logger.info(f"\tLOCAL tables created: {create_local_tables()}")
    logger.info(f"\tLOCAL triggers created: {check_local_rdbms.triggers()}")
    logger.info(f"\tLOCAL views created: {check_local_rdbms.views()}")
    logger.info(f"\tLOCAL stored proc(s) created: {check_local_rdbms.stored_procs()}")
    logger.info(
        f"--- COMPLETED LOCAL DATABASE SETUP ON: {my_secrets.prod_debian_dbhost} ---"
    )
    # POPULATE LOCAL
    logger.info(
        f"*** STARTED LOCAL DATABASE POPULATION ON: {my_secrets.prod_debian_dbhost} ***"
    )
    logger.info(f"\tLOCAL parcels table populated: {populate_local_tables.parcels()}")
    community_data_for_bluehost = populate_local_tables.communities()
    logger.info(
        f"\tLOCAL communities table populated: {len(community_data_for_bluehost) > 0}"
    )
    logger.info(
        f"--- COMPLETED LOCAL DATABASE POPULATION ON: {my_secrets.prod_debian_dbhost} ---"
    )
# CREATE REMOTE
# logger.info(f"*** STARTED REMOTE DATABASE SETUP ON: {my_secrets.prod_bluehost_dbhost} ***")
# logger.info((f"\tREMOTE tables check: {database_check_remote.tables()}"))
# logger.info(f"\tREMOTE schema check: {database_check_remote.schema()}")
# logger.info(f"\tREMOTE tables created: {database_check_remote.tables()}")
# logger.info(f"--- COMPLETED REMOTE DATABASE SETUP ON: {my_secrets.prod_bluehost_dbhost} ---")
# POPULATE REMOTE
# logger.info(f"*** STARTED REMOTE DATABASE POPULATION ON: {my_secrets.prod_bluehost_dbhost} ***")
# database_populate_remote.communities(community_data_for_bluehost)
# logger.info(f"--- COMPLETED REMOTE DATABASE POPULATION ON: {my_secrets.prod_bluehost_dbhost} ---")

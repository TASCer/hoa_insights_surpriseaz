# import logging

# from logging import Logger, Formatter
from sqlalchemy import create_engine
from hoa_insights_surpriseaz import my_secrets
from hoa_insights_surpriseaz.database import (
    check_local,
    #     check_remote,
    models,
    populate_local,
)
# from hoa_insights_surpriseaz.database import (
#     populate_remote,
# )

# root_logger: Logger = logging.getLogger()
# root_logger.setLevel(logging.INFO)

# fh = logging.FileHandler("__rdbms-creation__.log")
# fh.setLevel(logging.DEBUG)

# formatter: Formatter = logging.Formatter(
#     "%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s"
# )
# fh.setFormatter(formatter)

# root_logger.addHandler(fh)

TEST_LOCAL_DB_URI = f"{my_secrets.test_debian_uri}"
TEST_REMOTE_DB_HOSTNAME = f"{my_secrets.test_bluehost_dbname}"


# logger: Logger = logging.getLogger(__name__)

engine = create_engine(f"mysql+pymysql://{TEST_LOCAL_DB_URI}", echo=False)


def create_local_tables() -> bool:
    if check_local.schema(TEST_LOCAL_DB_URI):
        models.Base.metadata.create_all(engine)


if __name__ == "__main__":
    # CREATE LOCAL
    # logger.info(f"*** STARTED LOCAL TEST DATABASE SETUP ON: {my_secrets.prod_debian_dbhost} ***")
    create_local_tables()
    populate_local.parcels(datapath="./test_parcel_constants.csv", engine=engine)
    # community_data_for_bluehost = populate_local.communities()
    # logger.info(
    #     f"\tLOCAL communities table populated: {len(community_data_for_bluehost) > 0}"
    # )
    # logger.info(
    #     f"--- COMPLETED LOCAL DATABASE POPULATION ON: {my_secrets.prod_debian_dbhost} ---"
    # )
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

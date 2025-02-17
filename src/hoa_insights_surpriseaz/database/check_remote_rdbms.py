import logging
import sqlalchemy as sa

from logging import Logger
from sqlalchemy import create_engine, exc, types, Column, Table, MetaData
from sqlalchemy_utils import database_exists, create_database
from hoa_insights_surpriseaz import my_secrets
from hoa_insights_surpriseaz.database.local_models import Community, CommunityManagement

# REMOTE/BLUEHOST SQL DB CREDS
REMOTE_DB_HOSTNAME: str = f"{my_secrets.test_bluehost_dbhost}"
REMOTE_DB_NAME: str = f"{my_secrets.test_bluehost_dbname}"
REMOTE_DB_USER: str = f"{my_secrets.test_bluehost_dbuser}"
REMOTE_DB_PW: str = f"{my_secrets.test_bluehost_dbpass}"
REMOTE_DB_URI: str = f"{my_secrets.test_bluehost_uri}"

# REMOTE/BLUEHOST SQL TABLES
COMMUNITIES_TABLE: str = "communities"
COMMUNITY_MANAGENT_TABLE: str = "community_managers"

meta = MetaData()


def schema() -> bool:
    """Check to see if schema is present, if not, create and return True"""
    logger: Logger = logging.getLogger(__name__)
    try:
        engine = create_engine(f"mysql+pymysql://{REMOTE_DB_URI}")

        if not database_exists(engine.url):
            create_database(engine.url)

    except (exc.SQLAlchemyError, exc.OperationalError) as e:
        logger.critical(str(e))

        return False

    return True

# if __name__ == "__main__":
#     print(schema())
#     print(tables())

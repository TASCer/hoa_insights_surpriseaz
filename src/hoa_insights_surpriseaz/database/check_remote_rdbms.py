import logging

from hoa_insights_surpriseaz import my_secrets
from logging import Logger
from sqlalchemy import create_engine, exc, Engine
from sqlalchemy_utils import database_exists, create_database

REMOTE_DB_HOSTNAME: str = f"{my_secrets.prod_bluehost_dbhost}"
REMOTE_DB_NAME: str = f"{my_secrets.prod_bluehost_dbname}"
REMOTE_DB_USER: str = f"{my_secrets.prod_bluehost_dbuser}"
REMOTE_DB_PW: str = f"{my_secrets.prod_bluehost_dbpass}"
REMOTE_DB_URI: str = f"{my_secrets.prod_bluehost_uri}"


def schema() -> bool:
    """Check to see if schema is present, if not, create and return True"""
    logger: Logger = logging.getLogger(__name__)
    try:
        engine: Engine = create_engine(f"mysql+pymysql://{REMOTE_DB_URI}")

        if not database_exists(engine.url):
            create_database(engine.url)

    except (exc.SQLAlchemyError, exc.OperationalError) as e:
        logger.critical(str(e))

        return False

    return True

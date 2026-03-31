import logging
import os

from dotenv import load_dotenv
from logging import Logger
from sqlalchemy import Engine, text, exc

logger: Logger = logging.getLogger(__name__)

load_dotenv()

LOCAL_DB_NAME: str = f"{os.environ['PROD_LOCAL_DB_NAME']}"
LOCAL_DB_USER: str = f"{os.environ['PROD_LOCAL_DB_USER']}"

UPDATE_COMMUNITIES: str = "update_communities"


def all(engine: Engine) -> bool:
    """
    Function creates stored procedure(s).

    :param engine: database engine
    :return: True if created
    """
    try:
        with engine.connect() as conn, conn.begin():
            conn.execute(
                text(f"""CREATE DEFINER=`todd`@`%` PROCEDURE `{UPDATE_COMMUNITIES}`()
                BEGIN
                SELECT COMMUNITY , count(COMMUNITY) as COUNT FROM parcels group by COMMUNITY order by COMMUNITY;

                update communities
                    set COMMUNITY=COMMUNITY, COUNT=COUNT where COMMUNITY = COMMUNITY;

                END""")
            )
        logger.info(f"\t\t'{UPDATE_COMMUNITIES}' created")

    except exc.SQLAlchemyError as e:
        logger.critical(str(e))
        return False

    return True

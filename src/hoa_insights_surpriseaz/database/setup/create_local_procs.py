import logging

from hoa_insights_surpriseaz import my_secrets

from logging import Logger
from sqlalchemy import Engine, text, exc

logger: Logger = logging.getLogger(__name__)

LOCAL_DB_NAME: str = f"{my_secrets.prod_local_dbname}"
LOCAL_DB_USER: str = f"{my_secrets.prod_local_dbuser}"

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
        logger.info(f"'{UPDATE_COMMUNITIES}' created")

    except exc.SQLAlchemyError as e:
        logger.critical(str(e))
        return False

    return True

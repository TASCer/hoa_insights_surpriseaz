import logging
from logging import Logger

from sqlalchemy import Engine, exc, text

from hoa_insights_surpriseaz.database.config import UPDATE_COMMUNITIES

logger: Logger = logging.getLogger(__name__)


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

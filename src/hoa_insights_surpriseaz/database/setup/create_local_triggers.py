import logging

# from hoa_insights_surpriseaz.database import models_local
from hoa_insights_surpriseaz import my_secrets

from logging import Logger
from sqlalchemy import Engine, text, exc

logger: Logger = logging.getLogger(__name__)

LOCAL_DB_NAME: str = f"{my_secrets.prod_local_dbname}"
LOCAL_DB_USER: str = f"{my_secrets.prod_local_dbuser}"
OWNERS_TABLE: str = "owners"


def all(engine: Engine) -> bool:
    """
    Function creates a db engine and checks if schema, table, triggers, views are created.
    Returns a list of community totals for remote table population.
    """

    with engine.connect() as conn, conn.begin():
        try:
            conn.execute(text("DROP TRIGGER IF EXISTS after_sale_update"))
            trig_sales: str = f"""CREATE DEFINER=`{LOCAL_DB_USER}`@`%` TRIGGER `after_sale_update`
                            AFTER UPDATE ON `{OWNERS_TABLE}`
                            FOR EACH ROW BEGIN
                            IF OLD.SALE_DATE <> new.SALE_DATE THEN
                                INSERT IGNORE into historical_sales(apn,sale_date, sale_price, ts)
                                VALUES(OLD.APN,OLD.SALE_DATE, OLD.SALE_PRICE, CURRENT_TIME(6))
                                ON DUPLICATE KEY UPDATE SALE_DATE=OLD.SALE_DATE;
                            END IF;
                        END"""

            conn.execute(text(trig_sales))
            logger.info("TRIGGER: AFTER_SALE_UPDATE created")

            conn.execute(text("DROP TRIGGER IF EXISTS after_owner_update"))
            trig_owner: str = f"""CREATE DEFINER=`{LOCAL_DB_USER}`@`%` TRIGGER `after_owner_update`
                        AFTER UPDATE ON `owners`
                        FOR EACH ROW BEGIN
                            IF OLD.OWNER <> new.OWNER THEN
                                INSERT IGNORE into historical_owners(apn,owner,deed_date,deed_type, ts)
                                VALUES(OLD.APN,OLD.OWNER,OLD.DEED_DATE,OLD.DEED_TYPE, current_timestamp(6))
                                ON DUPLICATE KEY UPDATE DEED_DATE=OLD.DEED_DATE;
                            END IF;

                            IF OLD.RENTAL = 1 and new.RENTAL = 0 THEN
                                delete from rentals
                                where OLD.APN = APN;

                            END IF;
                    END"""

            conn.execute(text(trig_owner))
            logger.info("TRIGGER: AFTER_OWNER_UPDATE created")

        except exc.ProgrammingError as e:
            logger.critical(str(e))

        try:
            conn.execute(text("DROP TRIGGER IF EXISTS after_management_update"))
            trig_management: str = f"""CREATE DEFINER=`{LOCAL_DB_USER}`@`%` TRIGGER `after_management_update`
                            AFTER UPDATE ON `community_managers`
                            FOR EACH ROW BEGIN
                            IF OLD.MANAGER <> new.MANAGER THEN
                                INSERT IGNORE into historical_managers(COMMUNITY,BOARD_SITUS,BOARD_CITY,MANAGER,CONTACT_ADX,CONTACT_PH,ts)
                                VALUES(OLD.COMMUNITY,OLD.BOARD_SITUS,OLD.BOARD_CITY,OLD.MANAGER,OLD.CONTACT_ADX,OLD.CONTACT_PH,CURRENT_TIME(6))
                                ON DUPLICATE KEY UPDATE MANAGER=OLD.MANAGER, COMMUNITY=OLD.COMMUNITY;
                            END IF;
                        END"""

            conn.execute(text(trig_management))
            logger.info("TRIGGER: AFTER_MANAGEMENT_UPDATE created")

            return True

        except exc.ProgrammingError as e:
            logger.critical(str(e))

            return False

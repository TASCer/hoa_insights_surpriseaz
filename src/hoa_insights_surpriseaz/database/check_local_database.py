import logging

from logging import Logger
from sqlalchemy import (
    exc,
    Engine,
    text,
)
from sqlalchemy_utils import database_exists, create_database

from hoa_insights_surpriseaz import my_secrets

LOCAL_DB_NAME: str = f"{my_secrets.prod_local_dbname}"
LOCAL_DB_USER: str = f"{my_secrets.prod_local_dbuser}"

OWNERS_TABLE: str = "owners"
RENTALS_TABLE: str = "rentals"
MANAGEMENT_TABLE: str = "conmmunity_managers"

OWNERS_SALES_TRIGGER: str = "after_sale_update"

VIEW_COMMUNITY_RENTAL_TYPES: str = "community_rental_owner_types"
VIEW_TOP_RENTAL_TYPES: str = "top_rental_ownership_type"
VIEW_TOP_REGISTERED_RENTAL_OWNERS: str = "top_registered_rental_ownership"
VIEW_TOP_CLASSED_RENTAL_OWNERS: str = "top_classed_rental_ownership"
VIEW_TOP_RENTAL_OWNERS: str = "top_rental_ownership"
VIEW_REGISTERED_RENTALS: str = "registered_rentals"
VIEW_CLASSED_RENTALS: str = "classed_rentals"
VIEW_RENTAL_CONTACTS: str = "rental_contacts"
VIEW_COMMUNITY_SALES: str = "community_sales"

UPDATE_COMMUNITIES_SP: str = "update_communities"

logger: Logger = logging.getLogger(__name__)


def schema(engine: Engine) -> bool:
    """
    Function creates local database schema.

    :param engine: database engine
    :return: True if created
    """
    logger: Logger = logging.getLogger(__name__)

    try:
        if not database_exists(engine.url):
            create_database(engine.url)

    except (exc.SQLAlchemyError, exc.OperationalError) as e:
        logger.critical(str(e))
        return False

    return True


def triggers(engine: Engine) -> bool:
    """
    Function creates 'after_sale_update' and 'after_owner_update triggers on 'owners' table.

    :param engine: database engine
    :return: True if created
    """
    logger: Logger = logging.getLogger(__name__)

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
            logger.info("TRIGGER: AFTER_SALE_UPDATE has been created")
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
            logger.info("TRIGGER: AFTER_OWNER_UPDATE has been created")

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
            logger.info("TRIGGER: AFTER_MANAGEMENT_UPDATE has been created")

            return True

        except exc.ProgrammingError as e:
            logger.critical(str(e))

            return False


def views(engine: Engine) -> bool:
    """
    Function creates views for local database

    :param engine: database engine
    :return: True if created
    """
    try:
        with engine.connect() as conn, conn.begin():
            conn.execute(
                text(f"""
            CREATE OR REPLACE
                ALGORITHM = UNDEFINED 
                DEFINER = `todd`@`%` 
                SQL SECURITY DEFINER
            VIEW `{VIEW_COMMUNITY_RENTAL_TYPES}` AS
                SELECT 
                    `parcels`.`COMMUNITY` AS `COMMUNITY`,
                    `rentals`.`OWNER_TYPE` AS `OWNER_TYPE`,
                    COUNT('COMMUNITY') AS `total`
                FROM
                    (`{RENTALS_TABLE}`
                    JOIN `parcels` ON ((`rentals`.`APN` = `parcels`.`APN`)))
                GROUP BY `parcels`.`COMMUNITY` , `rentals`.`OWNER_TYPE`
            """)
            )
        logger.info(f"View: {VIEW_COMMUNITY_RENTAL_TYPES} created")

    except exc.SQLAlchemyError as e:
        logger.critical(str(e))
        return False

    try:
        with engine.connect() as conn, conn.begin():
            conn.execute(
                text(
                    f"""
            CREATE OR REPLACE
                ALGORITHM = UNDEFINED 
                DEFINER = `todd`@`%` 
                SQL SECURITY DEFINER
            VIEW `{VIEW_TOP_RENTAL_TYPES}` AS
                SELECT 
                    `rentals`.`OWNER_TYPE` AS `OWNER_TYPE`,
                    COUNT('OWNER_TYPE') AS `count`
                FROM
                    `rentals`
                GROUP BY `rentals`.`OWNER_TYPE`
                ORDER BY `count` DESC
            """
                )
            )
        logger.info(f"View: {VIEW_TOP_RENTAL_TYPES} created")

    except exc.SQLAlchemyError as e:
        logger.critical(str(e))
        return False

    # WEB VIEWS FOR LOCAL WEBSITE
    try:
        with engine.connect() as conn, conn.begin():
            conn.execute(
                text(
                    f"""
            CREATE OR REPLACE
                ALGORITHM = UNDEFINED 
                DEFINER = `todd`@`%` 
                SQL SECURITY DEFINER
            VIEW `{VIEW_REGISTERED_RENTALS}` AS
                SELECT 
                    `rentals`.`APN` AS `APN`,
                    `rentals`.`OWNER` AS `OWNER`,
                    `rentals`.`OWNER_TYPE` AS `OWNER_TYPE`,
                    `rentals`.`CONTACT` AS `CONTACT`,
                    `rentals`.`CONTACT_ADX` AS `CONTACT_ADX`,
                    `rentals`.`CONTACT_PH` AS `CONTACT_PH`,
                    `parcels`.`COMMUNITY` AS `COMMUNITY`,
                    `parcels`.`LAT` AS `LAT`,
                    `parcels`.`LONG` AS `LONG`,
                    `parcels`.`SITUS` AS `SITUS`
                FROM
                    (`rentals`
                    JOIN `parcels` ON ((`rentals`.`APN` = `parcels`.`APN`)))
            """
                )
            )
        logger.info(f"View: {VIEW_REGISTERED_RENTALS} created")

    except exc.SQLAlchemyError as e:
        logger.critical(str(e))
        return False

    try:
        with engine.connect() as conn, conn.begin():
            conn.execute(
                text(
                    f"""
            CREATE OR REPLACE
                ALGORITHM = UNDEFINED
                DEFINER = `todd`@`%`
                SQL SECURITY DEFINER
            VIEW `{VIEW_CLASSED_RENTALS}` AS
            SELECT
                `owners`.`OWNER` AS `OWNER`,
                `owners`.`LEGAL_CODE` AS `LEGAL_CODE`,
                `owners`.`MAIL_ADX` AS `MAIL_ADX`,
                `parcels`.`LAT` AS `LAT`,
                `parcels`.`LONG` AS `LONG`,
                `parcels`.`SITUS` AS `SITUS`,
                `parcels`.`APN` AS `APN`,
                `parcels`.`COMMUNITY` AS `COMMUNITY`
            FROM
                (`owners`
                JOIN `parcels` ON ((`owners`.`APN` = `parcels`.`APN`)))
            WHERE
                ((`owners`.`LEGAL_CODE` = '4.2')
                    AND (`owners`.`RENTAL` = 0))                
                    """
                )
            )
        logger.info(f"View: {VIEW_CLASSED_RENTALS} created")

    except exc.SQLAlchemyError as e:
        logger.critical(str(e))
        return False

    try:
        with engine.connect() as conn, conn.begin():
            conn.execute(
                text(
                    f"""
           CREATE OR REPLACE
                ALGORITHM = UNDEFINED 
                DEFINER = `todd`@`%` 
                SQL SECURITY DEFINER
            VIEW `{VIEW_TOP_REGISTERED_RENTAL_OWNERS}` AS
            SELECT 
                `registered_rentals`.`OWNER` AS `OWNER`,
                COUNT(`registered_rentals`.`OWNER`) AS `c`
            FROM
                `registered_rentals`
            GROUP BY `registered_rentals`.`OWNER`
            ORDER BY `c` DESC;      
                                """
                )
            )
        logger.info(f"View: {VIEW_TOP_REGISTERED_RENTAL_OWNERS} created")

    except exc.SQLAlchemyError as e:
        logger.critical(str(e))
        return False

    try:
        with engine.connect() as conn, conn.begin():
            conn.execute(
                text(
                    f"""
              CREATE OR REPLACE
                   ALGORITHM = UNDEFINED 
                   DEFINER = `todd`@`%` 
                   SQL SECURITY DEFINER
               VIEW `{VIEW_TOP_CLASSED_RENTAL_OWNERS}` AS
               SELECT 
                   `classed_rentals`.`OWNER` AS `OWNER`,
                   COUNT(`classed_rentals`.`OWNER`) AS `c`
               FROM
                   `classed_rentals`
               GROUP BY `classed_rentals`.`OWNER`
               ORDER BY `c` DESC;      
                                   """
                )
            )
        logger.info(f"View: {VIEW_TOP_CLASSED_RENTAL_OWNERS} created")

    except exc.SQLAlchemyError as e:
        logger.critical(str(e))
        return False

    try:
        with engine.connect() as conn, conn.begin():
            conn.execute(
                text(
                    f"""
              CREATE OR REPLACE
                   ALGORITHM = UNDEFINED 
                   DEFINER = `todd`@`%` 
                   SQL SECURITY DEFINER
               VIEW `{VIEW_RENTAL_CONTACTS}` AS
               SELECT 
                    `rentals`.`CONTACT` AS `CONTACT`,
                COUNT(`rentals`.`CONTACT`) AS `count`
                FROM
                    `rentals`
                GROUP BY `rentals`.`CONTACT` order by `count` desc;
                                            """
                )
            )
        logger.info(f"View: {VIEW_RENTAL_CONTACTS} created")

    except exc.SQLAlchemyError as e:
        logger.critical(str(e))
        return False

    try:
        with engine.connect() as conn, conn.begin():
            conn.execute(
                text(
                    f"""
              CREATE OR REPLACE
                   ALGORITHM = UNDEFINED 
                   DEFINER = `todd`@`%` 
                   SQL SECURITY DEFINER
               VIEW `{VIEW_TOP_RENTAL_OWNERS}` AS
               SELECT 
                    `reg`.`OWNER` AS `OWNER`, `cls`.`c` + `reg`.`c` AS `tot`
                FROM
                    (`top_classed_rental_ownership` `cls`
                JOIN `top_registered_rental_ownership` `reg` ON (`cls`.`OWNER` = `reg`.`OWNER`))
                ORDER BY `cls`.`c` + `reg`.`c` DESC"""
                )
            )
        logger.info(f"View: {VIEW_TOP_RENTAL_OWNERS} created")

    except exc.SQLAlchemyError as e:
        logger.critical(str(e))
        return False

    try:
        with engine.connect() as conn, conn.begin():
            conn.execute(
                text(
                    f"""CREATE 
            ALGORITHM = UNDEFINED 
            DEFINER = `todd`@`%` 
            SQL SECURITY DEFINER
        VIEW `{VIEW_COMMUNITY_SALES}` AS
            SELECT 
                `p`.`COMMUNITY` AS `COMMUNITY`,
                `o`.`SALE_DATE` AS `SALE_DATE`,
                `o`.`SALE_PRICE` AS `SALE_PRICE`
            FROM
                (`owners` `o`
                JOIN `parcels` `p` ON (`p`.`APN` = `o`.`APN`))
            WHERE
                YEAR(`o`.`SALE_DATE`) >= YEAR(CURRENT_TIMESTAMP())
                    AND YEAR(`o`.`SALE_DATE`) < YEAR(CURRENT_TIMESTAMP()) + 1"""
                )
            )

        logger.info(f"View: {VIEW_COMMUNITY_SALES} created")

    except exc.SQLAlchemyError as e:
        logger.critical(str(e))
        return False

    return True


# POC
def stored_procs(engine: Engine) -> bool:
    """
    Function creates a mySQL Stored Procedure to update communities.

    :param engine: database engine
    :return: True if created
    """
    try:
        with engine.connect() as conn, conn.begin():
            conn.execute(
                text(f"""CREATE DEFINER=`todd`@`%` PROCEDURE `{UPDATE_COMMUNITIES_SP}`()
                BEGIN
                SELECT COMMUNITY , count(COMMUNITY) as COUNT FROM parcels group by COMMUNITY order by COMMUNITY;

                update communities
                    set COMMUNITY=COMMUNITY, COUNT=COUNT where COMMUNITY = COMMUNITY;

                END""")
            )
        logger.info(f"StoredProc: {UPDATE_COMMUNITIES_SP} created")

    except exc.SQLAlchemyError as e:
        logger.critical(str(e))
        return False

    return True


if __name__ == "__main__":
    from sqlalchemy import create_engine

    LOCAL_DB_URI: str = f"{my_secrets.prod_local_uri}"
    engine: Engine = create_engine(f"mysql+pymysql://{LOCAL_DB_URI}", echo=False)
    triggers(engine=engine)

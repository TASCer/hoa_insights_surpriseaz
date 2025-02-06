import logging

from logging import Logger
from sqlalchemy import (
    create_engine,
    exc,
    MetaData,
    select,
    Engine,
    text,
    Row,
    TextClause,
)
from sqlalchemy_utils import database_exists, create_database
from typing import Sequence
from hoa_insights_surpriseaz import my_secrets

LOCAL_DB_HOSTNAME: str = f"{my_secrets.prod_debian_dbhost}"
LOCAL_DB_NAME: str = f"{my_secrets.prod_debian_dbname}"
LOCAL_DB_USER: str = f"{my_secrets.prod_debian_dbuser}"
LOCAL_DB_PW: str = f"{my_secrets.prod_debian_dbpass}"
LOCAL_DB_URI: str = f"{my_secrets.prod_debian_uri}"

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

UPDATE_COMMUNITIES_SP: str = "update_communities"

logger: Logger = logging.getLogger(__name__)


def schema(db_uri: str = LOCAL_DB_URI) -> bool:
    print(db_uri)
    """
    Function checks if schema/DB_NAME is present.
    Return True if it is.
    Return False and log error if not and could not be created.
    """
    logger: Logger = logging.getLogger(__name__)

    try:
        engine: Engine = create_engine(f"mysql+pymysql://{db_uri}")

        if not database_exists(engine.url):
            create_database(engine.url)

    except (exc.SQLAlchemyError, exc.OperationalError) as e:
        logger.critical(str(e))
        return False

    return True


def triggers(db_uri: str = LOCAL_DB_URI, db_name=LOCAL_DB_NAME) -> bool:
    """
    Function checks if 'after_sale_owners' and 'after_sale_update triggers are present on 'owners' table.
    Returns True if both are created.
    Returns False if either are missing and could not be created.
    """
    logger: Logger = logging.getLogger(__name__)

    try:
        engine: Engine = create_engine(f"mysql+pymysql://{db_uri}")

        _meta = MetaData()

    except exc.SQLAlchemyError as e:
        logger.critical(str(e))

        return False

    with engine.connect() as conn, conn.begin():
        q_owners_triggers: TextClause = select(
            text(
                f"* from INFORMATION_SCHEMA.TRIGGERS where EVENT_OBJECT_TABLE='{OWNERS_TABLE}';"
            )
        )
        owners_result: Sequence[Row] = conn.execute(q_owners_triggers)
        owners_triggers: list[str] = [x[1] for x in owners_result]

        q_management_trigger: TextClause = select(
            text(
                f"* from INFORMATION_SCHEMA.TRIGGERS where EVENT_OBJECT_TABLE='{MANAGEMENT_TABLE}';"
            )
        )
        management_result: Sequence[Row] = conn.execute(q_management_trigger)
        management_trigger: list[str] = [x[1] for x in management_result]

        # OWNERS TRIGGER
        if db_name in owners_triggers:
            return True

        else:
            try:
                conn.execute(text("DROP TRIGGER IF EXISTS after_sale_update"))
                trig_sales = f"""CREATE DEFINER=`{LOCAL_DB_USER}`@`%` TRIGGER `after_sale_update`
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

                trig_owner = f"""CREATE DEFINER=`{LOCAL_DB_USER}`@`%` TRIGGER `after_owner_update`
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

                # return True

            except exc.ProgrammingError as e:
                logger.critical(str(e))
                # return False

        # MANAGEMENT TRIGGER
        if LOCAL_DB_NAME in management_trigger:
            return True

        else:
            try:
                conn.execute(text("DROP TRIGGER IF EXISTS after_management_update"))
                trig_management = f"""CREATE DEFINER=`{LOCAL_DB_USER}`@`%` TRIGGER `after_management_update`
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


def views(db_uri: str = LOCAL_DB_URI) -> bool:
    """
    Function checks if views are present.
    Returns True if so.
    Returns False if any missing and could not be created.
    """
    try:
        engine = create_engine(f"mysql+pymysql://{db_uri}")
        _meta = MetaData()

    except exc.SQLAlchemyError as e:
        logger.critical(str(e))
        return False

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

    except exc.SQLAlchemyError as e:
        logger.critical(str(e))
        return False

    return True


# POC
def stored_procs(db_uri: str = LOCAL_DB_URI):
    try:
        engine: Engine = create_engine(f"mysql+pymysql://{db_uri}")

        _meta = MetaData()

    except exc.SQLAlchemyError as e:
        logger.critical(str(e))
        return False

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

    except exc.SQLAlchemyError as e:
        logger.critical(str(e))
        return False

    return True


if __name__ == "__main__":
    # print(views())
    print(triggers(f"{my_secrets.test_debian_uri}"))

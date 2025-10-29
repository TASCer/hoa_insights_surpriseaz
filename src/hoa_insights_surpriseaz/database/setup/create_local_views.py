import logging

# from hoa_insights_surpriseaz.database import models_local
from hoa_insights_surpriseaz import my_secrets

from logging import Logger
from sqlalchemy import Engine, text, exc

logger: Logger = logging.getLogger(__name__)

LOCAL_DB_NAME: str = f"{my_secrets.prod_local_dbname}"
LOCAL_DB_USER: str = f"{my_secrets.prod_local_dbuser}"

OWNERS_TABLE: str = "owners"
VIEW_COMMUNITY_RENTAL_TYPES: str = "community_rental_owner_types"
VIEW_TOP_RENTAL_TYPES: str = "top_rental_ownership_type"
VIEW_TOP_REGISTERED_RENTAL_OWNERS: str = "top_registered_rental_ownership"
VIEW_TOP_CLASSED_RENTAL_OWNERS: str = "top_classed_rental_ownership"
VIEW_TOP_RENTAL_OWNERS: str = "top_rental_ownership"
VIEW_REGISTERED_RENTALS: str = "registered_rentals"
VIEW_CLASSED_RENTALS: str = "classed_rentals"
VIEW_RENTAL_CONTACTS: str = "rental_contacts"
VIEW_COMMUNITY_SALES: str = "community_sales"

RENTALS_TABLE: str = "rentals"


def all(engine: Engine) -> bool:
    """
    _summary_

    :param engine: _description_
    :return: _description_
    """
    with engine.connect() as conn, conn.begin():
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
            logger.info(f"{VIEW_COMMUNITY_RENTAL_TYPES} created")

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
            logger.info(f"{VIEW_TOP_RENTAL_TYPES} created")

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
            logger.info(f"{VIEW_REGISTERED_RENTALS} created")

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
            logger.info(f"{VIEW_CLASSED_RENTALS} created")

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
            logger.info(f"{VIEW_TOP_REGISTERED_RENTAL_OWNERS} created")

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
            logger.info(f"{VIEW_TOP_CLASSED_RENTAL_OWNERS} created")

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
            logger.info(f"{VIEW_RENTAL_CONTACTS} created")

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
            logger.info(f"{VIEW_TOP_RENTAL_OWNERS} created")

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

            logger.info(f"{VIEW_COMMUNITY_SALES} created")

        except exc.SQLAlchemyError as e:
            logger.critical(str(e))
            return False

        return True

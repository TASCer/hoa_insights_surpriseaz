import logging

from hoa_insights_surpriseaz import my_secrets
from logging import Logger
from sqlalchemy import Engine, create_engine, exc, text

# from hoa_insights_surpriseaz.database.populate_local import PARCELS_TABLE

LOCAL_DB_HOSTNAME: str = f"{my_secrets.prod_debian_dbhost}"
LOCAL_DB_NAME: str = f"{my_secrets.prod_debian_dbname}"
LOCAL_DB_USER: str = f"{my_secrets.prod_debian_dbuser}"
LOCAL_DB_PW: str = f"{my_secrets.prod_debian_dbpass}"
LOCAL_DB_URI: str = f"{my_secrets.prod_debian_uri}"

OWNERS_TABLE: str = "owners"
RENTALS_TABLE: str = "rentals"


def owners(
    latest_parsed_owners, db_name: str = LOCAL_DB_NAME, db_uri: str = f"{LOCAL_DB_URI}"
) -> None:
    """
    Function takes in latest parsed API and sql data and updates the owners table.
    """
    if latest_parsed_owners is None:
        return

    logger: Logger = logging.getLogger(__name__)

    engine: Engine = create_engine(f"mysql+pymysql://{db_uri}")

    try:
        with engine.connect() as conn, conn.begin():
            delete_rentals = f"DELETE FROM {db_name}.{RENTALS_TABLE};"
            conn.execute(text(delete_rentals))

            for lo in latest_parsed_owners:
                try:
                    insert_qry = (
                        f"INSERT INTO {db_name}.{OWNERS_TABLE} (APN, OWNER, MAIL_ADX, SALE_DATE, SALE_PRICE, DEED_DATE, DEED_TYPE, LEGAL_CODE, RENTAL)"
                        f"VALUES('{lo.APN}', '{lo.OWNER}', '{lo.MAIL_ADX}', '{lo.SALE_DATE}', '{lo.SALE_PRICE}', '{lo.DEED_DATE}', '{lo.DEED_TYPE}', '{lo.LEGAL_CODE}', '{int(lo.RENTAL)}')"
                        f"ON DUPLICATE KEY UPDATE OWNER='{lo.OWNER}',MAIL_ADX='{lo.MAIL_ADX}',RENTAL='{int(lo.RENTAL)}', SALE_DATE='{lo.SALE_DATE}', SALE_PRICE='{lo.SALE_PRICE}', DEED_DATE='{lo.DEED_DATE}', DEED_TYPE='{lo.DEED_TYPE}', LEGAL_CODE='{lo.LEGAL_CODE}';"
                    )
                    conn.execute(text(insert_qry))

                except (
                    exc.SQLAlchemyError,
                    exc.ProgrammingError,
                    UnboundLocalError,
                ) as e:
                    logger.error(e)

    except exc.OperationalError as oe:
        logger.error(f"{oe.__cause__}: {LOCAL_DB_HOSTNAME}")
        logger.error("*** check server or run 'database_setup.py' if initial setup ***")
        print("Issue: CHECK TODAYS LOG or run 'database_setup.py' if initial setup")

        print(f"{oe.__cause__} -- RDBMS Issue: CHECK LOG")
        exit()


def rentals(latest_parsed_rentals, db_name: str = LOCAL_DB_NAME, db_uri: str = f"{LOCAL_DB_URI}") -> None:
    """
    Function takes in latest parsed API data with is_rental == 1
    updates the rentals table.
    """
    if latest_parsed_rentals is None:
        return

    logger: Logger = logging.getLogger(__name__)

    engine: Engine = create_engine(f"mysql+pymysql://{db_uri}")

    with engine.connect() as conn, conn.begin():
        delete_rentals: str = f"DELETE FROM {db_name}.{RENTALS_TABLE};"
        conn.execute(text(delete_rentals))

        for lr in latest_parsed_rentals:
            try:
                insert_qry = (
                    f"INSERT INTO {db_name}.{RENTALS_TABLE} (APN, OWNER, OWNER_TYPE, CONTACT, CONTACT_ADX, CONTACT_PH) "
                    f"VALUES('{lr.APN}', '{lr.OWNER}', '{lr.OWNER_TYPE}', '{lr.CONTACT}', '{lr.CONTACT_ADX}', '{lr.CONTACT_PH}')"
                    f"ON DUPLICATE KEY UPDATE OWNER='{lr.OWNER}', OWNER_TYPE='{lr.OWNER_TYPE}', CONTACT='{lr.CONTACT}', CONTACT_ADX='{lr.CONTACT_ADX}', CONTACT_PH='{lr.CONTACT_PH}';"
                )
                conn.execute(text(insert_qry))

            except exc.OperationalError as e:
                logger.error(e)

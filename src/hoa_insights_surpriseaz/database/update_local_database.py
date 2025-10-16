# TODO REWORK INSERTS - https://stackoverflow.com/questions/6611563/sqlalchemy-on-duplicate-key-update
import logging

from hoa_insights_surpriseaz import my_secrets
from logging import Logger
from sqlalchemy import Engine, create_engine, exc, text

LOCAL_DB_HOSTNAME: str = f"{my_secrets.prod_local_dbhost}"
LOCAL_DB_NAME: str = f"{my_secrets.prod_local_dbname}"
LOCAL_DB_USER: str = f"{my_secrets.prod_local_dbuser}"
LOCAL_DB_PW: str = f"{my_secrets.prod_local_dbpass}"
LOCAL_DB_URI: str = f"{my_secrets.prod_local_uri}"

OWNERS_TABLE: str = "owners"
RENTALS_TABLE: str = "rentals"


def owners(
    latest_parsed_owners: list, db_uri: str = LOCAL_DB_URI, db_name: str = LOCAL_DB_NAME
) -> None:
    """
    Function updates the local owners table.

    Args:
        latest_parsed_owners (list): Owner instances.
        db_uri (str, optional): Defaults to LOCAL_DB_URI.
        db_name (str, optional): Defaults to LOCAL_DB_NAME.
    """
    if latest_parsed_owners is None:
        return

    logger: Logger = logging.getLogger(__name__)

    engine: Engine = create_engine(f"mysql+pymysql://{db_uri}")

    try:
        with engine.connect() as conn, conn.begin():
            delete_rentals: str = f"DELETE FROM {db_name}.{RENTALS_TABLE};"
            conn.execute(text(delete_rentals))

            for owner in latest_parsed_owners:
                try:
                    insert_qry: str = (
                        f"INSERT INTO {db_name}.{OWNERS_TABLE} (APN, OWNER, MAIL_ADX, SALE_DATE, SALE_PRICE, DEED_DATE, DEED_TYPE, LEGAL_CODE, RENTAL)"
                        f"VALUES('{owner.APN}', '{owner.OWNER}', '{owner.MAIL_ADX}', '{owner.SALE_DATE}', '{owner.SALE_PRICE}', '{owner.DEED_DATE}', '{owner.DEED_TYPE}', '{owner.LEGAL_CODE}', '{int(owner.RENTAL)}')"
                        f"ON DUPLICATE KEY UPDATE OWNER='{owner.OWNER}',MAIL_ADX='{owner.MAIL_ADX}',RENTAL='{int(owner.RENTAL)}', SALE_DATE='{owner.SALE_DATE}', SALE_PRICE='{owner.SALE_PRICE}', DEED_DATE='{owner.DEED_DATE}', DEED_TYPE='{owner.DEED_TYPE}', LEGAL_CODE='{owner.LEGAL_CODE}';"
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
        exit()


def rentals(
    latest_parsed_rentals: list,
    db_name: str = LOCAL_DB_NAME,
    db_uri: str = LOCAL_DB_URI,
) -> None:
    """
    Function updates the local rentals table.

    Args:
        latest_parsed_rentals (list): Rentals instances.
        db_name (str, optional): Defaults to LOCAL_DB_NAME.
        db_uri (str, optional): Defaults to LOCAL_DB_URI.
    """
    if latest_parsed_rentals is None:
        return

    logger: Logger = logging.getLogger(__name__)

    engine: Engine = create_engine(f"mysql+pymysql://{db_uri}")

    with engine.connect() as conn, conn.begin():
        delete_rentals: str = f"DELETE FROM {db_name}.{RENTALS_TABLE};"
        conn.execute(text(delete_rentals))

        for rental in latest_parsed_rentals:
            try:
                insert_qry: str = (
                    f"INSERT INTO {db_name}.{RENTALS_TABLE} (APN, OWNER, OWNER_TYPE, CONTACT, CONTACT_ADX, CONTACT_PH) "
                    f"VALUES('{rental.APN}', '{rental.OWNER}', '{rental.OWNER_TYPE}', '{rental.CONTACT}', '{rental.CONTACT_ADX}', '{rental.CONTACT_PH}')"
                    f"ON DUPLICATE KEY UPDATE OWNER='{rental.OWNER}', OWNER_TYPE='{rental.OWNER_TYPE}', CONTACT='{rental.CONTACT}', CONTACT_ADX='{rental.CONTACT_ADX}', CONTACT_PH='{rental.CONTACT_PH}';"
                )
                conn.execute(text(insert_qry))

            except exc.OperationalError as e:
                logger.error(e)

import logging

from hoa_insights_surpriseaz import my_secrets
from logging import Logger
from sqlalchemy import Engine, create_engine, exc, text, Insert
from sqlalchemy.dialects.mysql import insert
from hoa_insights_surpriseaz.database import models_local

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

    :param latest_parsed_owners: sequence Owner instances
    :param db_uri: database identifier, defaults to LOCAL_DB_URI
    :param db_name: database name, defaults to LOCAL_DB_NAME
    """
    if latest_parsed_owners is None:
        return

    logger: Logger = logging.getLogger(__name__)

    engine: Engine = create_engine(f"mysql+pymysql://{db_uri}")

    try:
        with engine.connect() as conn, conn.begin():
            for owner in latest_parsed_owners:
                try:
                    insert_statement: Insert = insert(models_local.Owner).values(
                        APN=owner.APN,
                        OWNER=owner.OWNER,
                        MAIL_ADX=owner.MAIL_ADX,
                        SALE_DATE=owner.SALE_DATE,
                        SALE_PRICE=owner.SALE_PRICE,
                        DEED_DATE=owner.DEED_DATE,
                        DEED_TYPE=owner.DEED_TYPE,
                        LEGAL_CODE=owner.LEGAL_CODE,
                        RENTAL=int(owner.RENTAL),
                    )
                    upsert_statement: Insert = insert_statement.on_duplicate_key_update(
                        OWNER=owner.OWNER,
                        MAIL_ADX=owner.MAIL_ADX,
                        SALE_DATE=owner.SALE_DATE,
                        SALE_PRICE=owner.SALE_PRICE,
                        DEED_DATE=owner.DEED_DATE,
                        DEED_TYPE=owner.DEED_TYPE,
                        LEGAL_CODE=owner.LEGAL_CODE,
                        RENTAL=int(owner.RENTAL),
                    )
                    conn.execute(upsert_statement)

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
    Function updates the rentals table.

    :param latest_parsed_rentals: sequence Rental instances
    :param db_name: database name, defaults to LOCAL_DB_NAME
    :param db_uri: dtabase identifier, defaults to LOCAL_DB_URI
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
                insert_statement: Insert = insert(models_local.Rentals).values(
                    APN=rental.APN,
                    OWNER=rental.OWNER,
                    OWNER_TYPE=rental.OWNER_TYPE,
                    CONTACT=rental.CONTACT,
                    CONTACT_ADX=rental.CONTACT_ADX,
                    CONTACT_PH=rental.CONTACT_PH,
                )

                conn.execute(insert_statement)

            except exc.OperationalError as e:
                logger.error(e)

import logging
import sys
from logging import Logger

from sqlalchemy import Engine, Insert, create_engine, exc, text
from sqlalchemy.dialects.mysql import insert

from hoa_insights_surpriseaz.config import (
    PROD_LOCAL_DB_HOST,
    PROD_LOCAL_DB_NAME,
    PROD_LOCAL_DB_URI,
)
from hoa_insights_surpriseaz.database import models_local
from hoa_insights_surpriseaz.database.config import OWNERS_TABLE, RENTALS_TABLE

logger: Logger = logging.getLogger(__name__)


def owners(latest_parsed_owners: list, db_uri: str = PROD_LOCAL_DB_URI) -> None:
    """
    Function updates the local owners table.

    :param latest_parsed_owners: sequence Owner instances
    :param db_uri: database identifier, defaults to LOCAL_DB_URI
    # :param db_name: database name, defaults to LOCAL_DB_NAME
    """

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
        logger.error(f"{oe.__cause__}: '{PROD_LOCAL_DB_HOST}'")
        sys.exit()

    logger.info(f"\tTable: '{OWNERS_TABLE}' has been updated")


def rentals(
    latest_parsed_rentals: list,
    db_name: str = PROD_LOCAL_DB_NAME,
    db_uri: str = PROD_LOCAL_DB_URI,
) -> None:
    """
    Function updates the local rentals table.

    :param latest_parsed_rentals: sequence Rental instances
    :param db_name: database name, defaults to LOCAL_DB_NAME
    :param db_uri: database identifier, defaults to LOCAL_DB_URI
    """
    engine: Engine = create_engine(f"mysql+pymysql://{db_uri}")

    with engine.connect() as conn, conn.begin():
        delete_rentals: str = f"DELETE from {db_name}.{RENTALS_TABLE};"
        dropped = conn.execute(text(delete_rentals))
        print(dropped)
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

    logger.info(f"\tTable: '{RENTALS_TABLE}' has been updated")

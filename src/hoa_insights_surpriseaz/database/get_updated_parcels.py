import os
import logging

from dotenv import load_dotenv
from hoa_insights_surpriseaz.database.models_local import (
    HistoricalSales,
    HistoricalOwners,
    Parcel,
)
from hoa_insights_surpriseaz.utils.date_parser import sql_date
from logging import Logger
from sqlalchemy import (
    Engine,
    create_engine,
    exc,
    CursorResult,
    select,
)
from typing import Any

load_dotenv()

LOCAL_DB_URI: str = f"{os.environ['PROD_LOCAL_DB_URI']}"


def changes(db_uri: str = f"{LOCAL_DB_URI}") -> tuple[list[str], list[str]]:
    """
    Function determines updates to parcels by querying historical_sales and historical_owners tables with a TS(timestamp) of today.

    :param db_uri: database identifier, defaults to f"{LOCAL_DB_URI}"
    :return: list of owner changes and list of sale changes
    """
    logger: Logger = logging.getLogger(__name__)
    engine: Engine = create_engine(f"mysql+pymysql://{db_uri}")

    with engine.connect() as conn, conn.begin():
        try:
            q_sales: CursorResult[Any] = conn.execute(
                select(
                    HistoricalSales.APN,
                    Parcel.COMMUNITY,
                    HistoricalSales.SALE_DATE,
                    HistoricalSales.SALE_PRICE,
                )
                .join(Parcel, onclause=HistoricalSales.APN == Parcel.APN)
                .where(HistoricalSales.TS.like(f"{sql_date()}%"))
            )

            q_owners: CursorResult[Any] = conn.execute(
                select(
                    HistoricalOwners.APN,
                    Parcel.COMMUNITY,
                    HistoricalOwners.OWNER,
                    HistoricalOwners.DEED_DATE,
                    HistoricalOwners.DEED_TYPE,
                )
                .join(Parcel, onclause=HistoricalOwners.APN == Parcel.APN)
                .where(HistoricalOwners.TS.like(f"{sql_date()}%"))
            )

        except exc.OperationalError as e:
            logger.critical(str(e))
            exit()
        sales_updates: list = [x for x in q_sales]
        owners_updates: list = [x for x in q_owners]

    return owners_updates, sales_updates


if __name__ == "__main__":
    print(changes())

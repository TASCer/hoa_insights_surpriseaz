import logging
import os
import sys
from logging import Logger
from typing import Any

from dotenv import load_dotenv
from sqlalchemy import (
    CursorResult,
    Engine,
    create_engine,
    exc,
    select,
)

from hoa_insights_surpriseaz.database.models_local import (
    HistoricalOwners,
    HistoricalSales,
    Owner,
    Parcel,
)
from hoa_insights_surpriseaz.utils.date_parser import sql_date

load_dotenv()

LOCAL_DB_URI: str = f"{os.environ['PROD_LOCAL_DB_URI']}"


def changes(
    db_uri: str = f"{LOCAL_DB_URI}",
) -> tuple[list[str], list[str], list[str], list[str]]:
    """
    Function determines updates to parcels by querying historical_sales and historical_owners tables with a TS(timestamp) of today.

    :param db_uri: database identifier, defaults to f"{LOCAL_DB_URI}"
    :return: list of owner changes and list of sale changes
    """
    logger: Logger = logging.getLogger(__name__)
    engine: Engine = create_engine(f"mysql+pymysql://{db_uri}")

    with engine.connect() as conn, conn.begin():
        try:
            q_old_sales: CursorResult[Any] = conn.execute(
                statement=select(
                    HistoricalSales.APN,
                    Parcel.COMMUNITY,
                    HistoricalSales.SALE_DATE,
                    HistoricalSales.SALE_PRICE,
                )
                .join(target=Parcel, onclause=HistoricalSales.APN == Parcel.APN)
                .where(HistoricalSales.TS.like(f"{sql_date()}%"))
            )
            old_sales: list = [x for x in q_old_sales]

            q_old_owners: CursorResult[Any] = conn.execute(
                statement=select(
                    HistoricalOwners.APN,
                    Parcel.COMMUNITY,
                    HistoricalOwners.OWNER,
                    HistoricalOwners.DEED_DATE,
                    HistoricalOwners.DEED_TYPE,
                )
                .join(target=Parcel, onclause=HistoricalOwners.APN == Parcel.APN)
                .where(HistoricalOwners.TS.like(f"{sql_date()}%"))
            )
            old_owners: list = [x for x in q_old_owners]

            q_new_sales: CursorResult[Any] = conn.execute(
                statement=select(
                    Owner.APN,
                    Parcel.COMMUNITY,
                    Owner.SALE_DATE,
                    Owner.SALE_PRICE,
                )
                .join(target=Parcel, onclause=Owner.APN == Parcel.APN)
                .where(Owner.APN.in_(other=[x[0] for x in old_sales]))
            )
            new_sales: list = [x for x in q_new_sales]

            q_new_owners: CursorResult[Any] = conn.execute(
                statement=select(
                    Owner.APN,
                    Parcel.COMMUNITY,
                    Owner.OWNER,
                    Owner.DEED_DATE,
                    Owner.DEED_TYPE,
                )
                .join(target=Parcel, onclause=Owner.APN == Parcel.APN)
                .where(Owner.APN.in_([x[0] for x in old_owners]))
            )

            new_owners: list = [x for x in q_new_owners]

        except exc.OperationalError:
            logger.exception("db issue")
            sys.exit()

    return new_owners, old_owners, new_sales, old_sales


if __name__ == "__main__":
    print(changes())

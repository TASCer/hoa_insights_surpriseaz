import logging

from logging import Logger
from sqlalchemy import Engine, create_engine, exc, text
from hoa_insights_surpriseaz.utils.date_parser import sql_date
from hoa_insights_surpriseaz import my_secrets

LOCAL_DB_URI = f"{my_secrets.prod_debian_uri}"


def changes(db_uri: str = f"{LOCAL_DB_URI}") -> tuple[list]:
    """
    Function queries historical_sales and historical_owners tables with a TS(timestamp) of today.
    Returns tuple of sale change list and owner change list.
    """
    logger: Logger = logging.getLogger(__name__)
    engine: Engine = create_engine(f"mysql+pymysql://{db_uri}")

    with engine.connect() as conn, conn.begin():
        try:
            q_sales = conn.execute(
                text(
                    f"SELECT hs.APN, c.COMMUNITY, hs.SALE_DATE, hs.SALE_PRICE from historical_sales hs inner join parcels c on hs.APN = c.APN where DATE(TS) = '{sql_date()}'"
                )
            )
            q_owners = conn.execute(
                text(
                    f"SELECT ho.APN, c.COMMUNITY, ho.OWNER, ho.DEED_DATE, ho.DEED_TYPE from historical_owners ho inner join parcels c on ho.APN = c.APN where DATE(TS) = '{sql_date()}'"
                )
            )

        except exc.OperationalError as e:
            logger.critical(str(e))
            exit()
        sales_updates: list = [x for x in q_sales]
        owners_updates: list = [x for x in q_owners]

    return owners_updates, sales_updates


if __name__ == "__main__":
    owners, sales = changes()
    print(owners)

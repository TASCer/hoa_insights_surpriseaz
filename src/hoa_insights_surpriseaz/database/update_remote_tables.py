import logging

from hoa_insights_surpriseaz.utils.date_parser import get_now
from hoa_insights_surpriseaz import my_secrets
from logging import Logger
from pandas import Series, DataFrame, read_csv
from pathlib import Path
from sqlalchemy import Engine, TextClause, create_engine, exc, text

LOCAL_DB_URI: str = f"{my_secrets.prod_debian_uri}"
REMOTE_DB_URI: str = f"{my_secrets.prod_bluehost_uri}"

FINANCIAL_YTD_CSV_PATH = (
    Path.cwd() / "output" / "csv" / "financial" / "ytd_community_avg_sale_price.csv"
)


def get_ytd_community_avg_sale() -> DataFrame:
    data: DataFrame = read_csv(f"{FINANCIAL_YTD_CSV_PATH}")
    return data


def all() -> None:
    """
    Function gets all rental parcels from local database views, last table update, and community sales
    and populates remote databases tables for web site.
    """
    logger: Logger = logging.getLogger(__name__)

    try:
        engine: Engine = create_engine(f"mysql+pymysql://{LOCAL_DB_URI}")
        with engine.connect() as conn, conn.begin():
            q_registered_rentals: TextClause = conn.execute(
                text("""SELECT * FROM registered_rentals;""")
            )
            q_classed_rentals: TextClause = conn.execute(
                text("""SELECT * FROM classed_rentals;""")
            )
            q_rental_owner_types: TextClause = conn.execute(
                text("""SELECT * FROM community_rental_owner_types;""")
            )

    except exc.DBAPIError as db_err:
        logger.error(str(db_err))

    registered: list = [r for r in q_registered_rentals]
    registered_rentals: DataFrame = DataFrame(registered)

    classed: list = [c for c in q_classed_rentals]
    classed_rentals: DataFrame = DataFrame(classed)

    community_rental_owners = [o for o in q_rental_owner_types]
    community_rental_owner_types = DataFrame(community_rental_owners)

    logger.info(f"REGISTERED RENTALS: {len(registered_rentals)}")
    logger.info(f"CLASSED RENTALS: {len(classed_rentals)}")

    try:
        logger: Logger = logging.getLogger(__name__)
        engine: Engine = create_engine(f"mysql+pymysql://{REMOTE_DB_URI}")

        with engine.connect() as conn, conn.begin():
            community_sales: DataFrame = get_ytd_community_avg_sale()

            try:
                registered_rentals.to_sql(
                    name="registered_rentals",
                    con=conn,
                    if_exists="replace",
                    index=False,
                )
                logger.info("\tTable 'registered_rentals' has been updated REMOTELY")

                classed_rentals.to_sql(
                    name="classed_rentals",
                    con=conn,
                    if_exists="replace",
                    index=False,
                )
                logger.info("\tTable: 'classed_rentals' has been updated REMOTELY")

                community_sales.to_sql(
                    name="community_sales",
                    con=conn,
                    if_exists="replace",
                    index=False,
                )
                logger.info("\tTable: 'community_sales' has been updated REMOTELY")

                community_rental_owner_types.to_sql(
                    name="community_rental_owner_types",
                    con=conn,
                    if_exists="replace",
                    index=False,
                )
                logger.info(
                    "\tTable: 'community_rental_owners' has been updated REMOTELY"
                )

                Series(get_now(), name="TS").to_sql(
                    name="last_updated",
                    con=conn,
                    if_exists="replace",
                    index=False,
                )
                logger.info("\tTable: 'last_updated' has been updated REMOTELY")

            except exc.SQLAlchemyError as e:
                logger.critical(repr(e))

    except exc.OperationalError as e:
        logger.critical(repr(e))


if __name__ == "__main__":
    all()

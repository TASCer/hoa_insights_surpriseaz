import logging

from hoa_insights_surpriseaz.utils.date_parser import get_now
from hoa_insights_surpriseaz import my_secrets
from logging import Logger
from pandas import Series, DataFrame
from sqlalchemy import Engine, TextClause, create_engine, exc, text

LOCAL_DB_URI: str = f"{my_secrets.prod_local_uri}"
REMOTE_DB_URI: str = f"{my_secrets.prod_remote_uri}"

logger: Logger = logging.getLogger(__name__)


def financial_tables(
    local_db: str = LOCAL_DB_URI, remote_db: str = REMOTE_DB_URI
) -> None:
    """
    Function updates remote finance tables.

    :param local_db: local database identifier, defaults to LOCAL_DB_URI
    :param remote_db: remote database identifier, defaults to REMOTE_DB_URI
    """
    try:
        engine: Engine = create_engine(f"mysql+pymysql://{local_db}")
        with engine.connect() as conn, conn.begin():
            q_community_sales: TextClause = conn.execute(
                text("""SELECT * FROM community_sales;""")
            )
    except exc.DBAPIError as db_err:
        logger.error(str(db_err))

    ytd_sales = [s for s in q_community_sales]
    community_sales: DataFrame = DataFrame(ytd_sales)

    try:
        engine: Engine = create_engine(f"mysql+pymysql://{remote_db}")
        with engine.connect() as conn, conn.begin():
            if len(community_sales) >= 1:
                community_sales.to_sql(
                    name="community_sales",
                    con=conn,
                    if_exists="replace",
                    index=False,
                )
            logger.info(f"YTD SALES: {len(community_sales)}")

    except exc.OperationalError as e:
        logger.critical(repr(e))


def rental_tables(local_db: str = LOCAL_DB_URI, remote_db: str = REMOTE_DB_URI) -> None:
    """
    Function updates remote rentals tables.

    :param local_db: local database identifier, defaults to LOCAL_DB_URI
    :param remote_db: remote database identifier, defaults to REMOTE_DB_URI
    """
    try:
        engine: Engine = create_engine(f"mysql+pymysql://{local_db}")
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
    community_rental_owner_types: DataFrame = DataFrame(community_rental_owners)

    logger.info(f"REGISTERED RENTALS: {len(registered_rentals)}")
    logger.info(f"CLASSED RENTALS: {len(classed_rentals)}")

    try:
        engine: Engine = create_engine(f"mysql+pymysql://{remote_db}")

        with engine.connect() as conn, conn.begin():
            if len(registered_rentals) >= 1:
                registered_rentals.to_sql(
                    name="registered_rentals",
                    con=conn,
                    if_exists="replace",
                    index=False,
                )
                logger.info("\tTable: 'registered_rentals' has been updated")

            if len(classed_rentals) >= 1:
                classed_rentals.to_sql(
                    name="classed_rentals",
                    con=conn,
                    if_exists="replace",
                    index=False,
                )
                logger.info("\tTable: 'classed_rentals' has been updated")

            if len(community_rental_owner_types) >= 1:
                community_rental_owner_types.to_sql(
                    name="community_rental_owner_types",
                    con=conn,
                    if_exists="replace",
                    index=False,
                )
                logger.info("\tTable: 'community_rental_owners' has been updated")

                logger.info("\tTable: 'last_updated' has been updated")

            Series(get_now(), name="TS").to_sql(
                name="last_updated",
                con=conn,
                if_exists="replace",
                index=False,
            )

    except exc.OperationalError as e:
        logger.critical(repr(e))


if __name__ == "__main__":
    financial_tables()
    rental_tables()

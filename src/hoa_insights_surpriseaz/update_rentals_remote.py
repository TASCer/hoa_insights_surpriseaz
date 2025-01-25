import logging
import pandas as pd

from logging import Logger
from sqlalchemy import create_engine, exc, text
from hoa_insights_surpriseaz.utils.date_parser import sql_timestamp
from hoa_insights_surpriseaz import my_secrets

LOCAL_DB_URI: str = f"{my_secrets.debian_uri}"
REMOTE_DB_URI: str = f"{my_secrets.bluehost_uri}"


def update() -> None:
    """
    Gets all rental parcel data from local database views and populates remote databases for web site.
    """
    logger: Logger = logging.getLogger(__name__)
    try:
        engine = create_engine(f"mysql+pymysql://{LOCAL_DB_URI}")
        with engine.connect() as conn, conn.begin():
            q_registered_rentals = conn.execute(
                text("""SELECT * FROM registered_rentals;""")
            )
            q_classed_rentals = conn.execute(text("""SELECT * FROM classed_rentals;"""))

    except exc.DBAPIError as db_err:
        logger.error(str(db_err))

    registered: list = [x for x in q_registered_rentals]
    registered_rentals: pd.DataFrame = pd.DataFrame(registered)

    classed: list = [x for x in q_classed_rentals]
    classed_rentals: pd.DataFrame = pd.DataFrame(classed)

    logger.info(
        f"Registered Rentals: {len(registered_rentals)} - Classed Rentals - {len(classed_rentals)}"
    )

    try:
        logger: Logger = logging.getLogger(__name__)
        engine = create_engine(f"mysql+pymysql://{REMOTE_DB_URI}")

        with engine.connect() as conn, conn.begin():
            try:
                registered_rentals.to_sql(
                    name="registered_rentals",
                    con=conn,
                    if_exists="replace",
                    index=False,
                )
                logger.info("Table 'registered_rentals' has been updated REMOTELY")

                classed_rentals.to_sql(
                    name="classed_rentals",
                    con=conn,
                    if_exists="replace",
                    index=False,
                )
                logger.info("Table: 'classed_rentals' has been updated REMOTELY")

                pd.Series(sql_timestamp()).to_sql(
                    name="last_updated",
                    con=conn,
                    if_exists="replace",
                    index=False,
                )
                logger.info("Table: 'last_updated' has been updated REMOTELY")

            except exc.SQLAlchemyError as e:
                logger.critical(repr(e))

    except exc.OperationalError as e:
        logger.critical(repr(e))


if __name__ == "__main__":
    update()

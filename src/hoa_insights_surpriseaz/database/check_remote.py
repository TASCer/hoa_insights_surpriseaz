import logging
import sqlalchemy as sa

from logging import Logger
from sqlalchemy import create_engine, exc, types, Column, Table, MetaData
from sqlalchemy_utils import database_exists, create_database
from hoa_insights_surpriseaz import my_secrets

# REMOTE/BLUEHOST SQL DB CREDS
REMOTE_DB_HOSTNAME: str = f"{my_secrets.bluehost_dbhost}"
REMOTE_DB_NAME: str = f"{my_secrets.bluehost_dbname}"
REMOTE_DB_USER: str = f"{my_secrets.bluehost_dbuser}"
REMOTE_DB_PW: str = f"{my_secrets.bluehost_dbpass}"
REMOTE_DB_URI: str = f"{my_secrets.bluehost_uri}"

# REMOTE/BLUEHOST SQL TABLES
COMMUNITY_TOTALS: str = "communities"
COMMUNITY_MANAGENT: str = "community_managers"

meta = MetaData()


def schema() -> bool:
    """Check to see if schema is present, if not, create and return True"""
    logger: Logger = logging.getLogger(__name__)
    try:
        engine = create_engine(f"mysql+pymysql://{REMOTE_DB_URI}")

        if not database_exists(engine.url):
            create_database(engine.url)

    except (exc.SQLAlchemyError, exc.OperationalError) as e:
        logger.critical(str(e))

        return False

    return True


def tables():
    """
    Check to see if all required tables are created
    If not, create them and return True
    Returns False and logs if error in creating
    """
    logger: Logger = logging.getLogger(__name__)

    try:
        engine = create_engine(f"mysql+pymysql://{REMOTE_DB_URI}")

    except (exc.SQLAlchemyError, exc.OperationalError) as e:
        logger.critical(str(e))

        return False

    communities_tbl_insp = sa.inspect(engine)
    communities_tbl = communities_tbl_insp.has_table(
        COMMUNITY_TOTALS, schema=f"{REMOTE_DB_NAME}"
    )

    community_management_tbl_insp = sa.inspect(engine)
    community_management_tbl = community_management_tbl_insp.has_table(
        COMMUNITY_MANAGENT, schema=f"{REMOTE_DB_NAME}"
    )

    if not communities_tbl:
        engine = create_engine(f"mysql+pymysql://{REMOTE_DB_URI}")

        _communities = Table(
            COMMUNITY_TOTALS,
            meta,
            Column("COMMUNITY", types.VARCHAR(100), primary_key=True),
            Column("LAT", types.DOUBLE_PRECISION(), primary_key=True),
            Column("LONG", types.DOUBLE_PRECISION(), primary_key=True),
            Column("COUNT", types.INT),
            Column("MANAGED_ID", types.INT),
        )

    if not community_management_tbl:
        engine = create_engine(f"mysql+pymysql://{REMOTE_DB_URI}")

        _community_managers = Table(
            COMMUNITY_MANAGENT,
            meta,
            Column("ID", types.INT, primary_key=True),
            Column("COMMUNITY", types.VARCHAR(100)),
            Column("BOARD_SITUS", types.VARCHAR(60)),
            Column("BOARD_CITY", types.VARCHAR(60)),
            Column("MANAGER", types.VARCHAR(100)),
            Column("CONTACT_ADX", types.VARCHAR(120)),
            Column("CONTACT_PH", types.VARCHAR(120)),
        )

    meta.create_all(engine)

    return True


if __name__ == "__main__":
    print(schema())
    print(tables())

import logging

from hoa_insights_surpriseaz import my_secrets
from hoa_insights_surpriseaz.database.setup import (
    create_local_database,
    create_remote_database,
)
from logging import Logger, Formatter
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

root_logger: Logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

fh = logging.FileHandler("__database-setup__.log")
fh.setLevel(logging.DEBUG)

formatter: Formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s"
)
fh.setFormatter(formatter)

root_logger.addHandler(fh)

logger: Logger = logging.getLogger(__name__)

LOCAL_DB_URI: str = f"{my_secrets.prod_local_uri}"
REMOTE_DB_URI: str = f"{my_secrets.prod_remote_uri}"


def main():
    LOCAL_ENGINE: Engine = create_engine(f"mysql+pymysql://{LOCAL_DB_URI}", echo=False)
    REMOTE_ENGINE: Engine = create_engine(
        f"mysql+pymysql://{REMOTE_DB_URI}", echo=False
    )

    local_session = Session(LOCAL_ENGINE)

    community_totals, local_db = create_local_database.create(
        engine=LOCAL_ENGINE, session=local_session
    )

    remote_session = Session(REMOTE_ENGINE)

    create_remote_database.create(
        community_totals=community_totals,
        remote_engine=REMOTE_ENGINE,
        local_db=local_session,
    )

    logger.info(
        f"DATABASES: {LOCAL_ENGINE.url.database}, {REMOTE_ENGINE.url.database} INITIALIZED."
    )


if __name__ == "__main__":
    main()

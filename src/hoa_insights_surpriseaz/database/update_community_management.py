import csv
import logging

from hoa_insights_surpriseaz.database.models_local import CommunityManagement as DBCM
from hoa_insights_surpriseaz.schemas import CommunityManagement as SCM
from hoa_insights_surpriseaz import my_secrets
from hoa_insights_surpriseaz.database.check_remote_rdbms import REMOTE_DB_NAME
from hoa_insights_surpriseaz.database.check_local_rdbms import LOCAL_DB_NAME
from logging import Logger
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy import Engine, create_engine, exc, TextClause, text
from typing import TextIO

LOCAL_DB_URI: str = f"{my_secrets.prod_debian_uri}"
REMOTE_DB_URI: str = f"{my_secrets.prod_bluehost_uri}"

logger: Logger = logging.getLogger(__name__)

MANAGEMENT_TABLE: str = "community_managers"


def get_communities(parsed_csv: str) -> list[str]:
    """
    Function takes in the path of the management pdf file that was downloaded and parsed to csv.
    Reads the file and creates a row for each community and drops the header.
    Returns list of str.
    """

    try:
        with open(parsed_csv, "r") as f:
            reader: TextIO = csv.reader(f)
            communitities: list = [c for c in reader]
            communitities.pop(0)

            return communitities

    except FileNotFoundError as ffe:
        logger.addFilter(f"{ffe}")


def update(file: str = None) -> None:
    """
    Function updates the community_managers tables (local, remote) with data from the monthly pdf download.
    """
    community_managers: list = get_communities(file)

    local_engine: Engine = create_engine(f"mysql+pymysql://{LOCAL_DB_URI}", echo=False)

    with Session(local_engine) as ls:
        for m in community_managers:
            id, community, situs, city, ph, email, mgr = m
            id = int(id) + 1

            item = SCM(
                COMMUNITY=community,
                BOARD_SITUS=situs,
                BOARD_CITY=city,
                MANAGER=mgr,
                CONTACT_ADX=email,
                CONTACT_PH=ph,
            )
            db_item = DBCM(**item.model_dump())

            try:
                insert_qry: TextClause = f"""UPDATE {LOCAL_DB_NAME}.{MANAGEMENT_TABLE} 
                SET BOARD_SITUS='{db_item.BOARD_SITUS}', BOARD_CITY='{db_item.BOARD_CITY}', MANAGER='{db_item.MANAGER}', CONTACT_ADX='{db_item.CONTACT_ADX}', CONTACT_PH='{db_item.CONTACT_PH}'
                WHERE ID = '{id}'
                    ;"""

                ls.execute(text(insert_qry))
                ls.commit()

            except exc.OperationalError as e:
                logger.error(e)

    remote_engine: Engine = create_engine(
        f"mysql+pymysql://{REMOTE_DB_URI}", echo=False
    )

    with Session(remote_engine) as rs:
        for m in community_managers:
            id, community, situs, city, ph, email, mgr = m
            id = int(id) + 1

            item = SCM(
                COMMUNITY=community,
                BOARD_SITUS=situs,
                BOARD_CITY=city,
                MANAGER=mgr,
                CONTACT_ADX=email,
                CONTACT_PH=ph,
            )
            db_item = DBCM(**item.model_dump())

            try:
                insert_qry: TextClause = f"""UPDATE {REMOTE_DB_NAME}.{MANAGEMENT_TABLE} 
                SET BOARD_SITUS='{db_item.BOARD_SITUS}', BOARD_CITY='{db_item.BOARD_CITY}', MANAGER='{db_item.MANAGER}', CONTACT_ADX='{db_item.CONTACT_ADX}', CONTACT_PH='{db_item.CONTACT_PH}'
                WHERE ID = '{id}'
                    ;"""

                rs.execute(text(insert_qry))
                rs.commit()

            except exc.OperationalError as e:
                logger.error(e)


if __name__ == "__main__":
    CSV_PATH: Path = Path.cwd().parent / "output" / "csv"
    CSV_FILENAME: str = "surpriseaz-hoa-management.csv"
    PDF_NEW_FILENAME: str = "MANAGEMENT.pdf"
    PDF_PATH: Path = Path.cwd() / "output" / "pdf"
    print(update(CSV_PATH / CSV_FILENAME))

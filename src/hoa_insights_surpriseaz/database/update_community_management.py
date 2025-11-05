import csv
import logging

from hoa_insights_surpriseaz.database.models_local import (
    CommunityManagement as MODEL_CM,
)
from hoa_insights_surpriseaz.schemas import CommunityManagement as SCHEMA_CM
from hoa_insights_surpriseaz import my_secrets

from logging import Logger
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy import Engine, create_engine, exc, update, Update

LOCAL_DB_URI: str = f"{my_secrets.prod_local_uri}"
REMOTE_DB_URI: str = f"{my_secrets.prod_remote_uri}"

logger: Logger = logging.getLogger(__name__)

MANAGEMENT_TABLE: str = "community_managers"


def get_communities(parsed_csv: Path) -> list[str]:
    """
    Function collects managed communities from file.

    :param parsed_csv: from monthly  connunity managemeent update.
    :return: managed communities
    """
    try:
        with open(parsed_csv, "r") as f:
            reader = csv.reader(f)
            communitities: list[str] = [c for c in reader]
            communitities.pop(0)

    except FileNotFoundError as ffe:
        communitities = []
        logger.addFilter(f"{ffe}")

    return communitities


def update_local_table(community_managers: list) -> None:
    """
    Function updates the local community_managers table with data from the monthly pdf download.

    :param file: management csv
    """
    logger.info(f"updating local table: {MANAGEMENT_TABLE}")
    local_engine: Engine = create_engine(f"mysql+pymysql://{LOCAL_DB_URI}", echo=False)
    with Session(local_engine) as local_session:
        for manager in community_managers:
            m_id, community, situs, city, ph, email, mgr = manager
            m_id: int = int(m_id) + 1

            manager_instance = SCHEMA_CM(
                COMMUNITY=community,
                BOARD_SITUS=situs,
                BOARD_CITY=city,
                MANAGER=mgr,
                CONTACT_ADX=email,
                CONTACT_PH=ph,
            )
            db_item = MODEL_CM(**manager_instance.model_dump())

            try:
                update_statement: Update = (
                    update(MODEL_CM)
                    .where(MODEL_CM.ID == m_id)
                    .values(
                        ID=m_id,
                        BOARD_SITUS=db_item.BOARD_SITUS,
                        BOARD_CITY=db_item.BOARD_CITY,
                        MANAGER=db_item.MANAGER,
                        CONTACT_ADX=db_item.CONTACT_ADX,
                        CONTACT_PH=db_item.CONTACT_PH,
                    )
                )

                local_session.execute(update_statement)
                local_session.commit()

            except exc.OperationalError as e:
                logger.error(e)

    logger.info(f"updated local table: {MANAGEMENT_TABLE}")


def update_remote_table(community_managers: list) -> None:
    remote_engine: Engine = create_engine(
        f"mysql+pymysql://{REMOTE_DB_URI}", echo=False
    )
    """
    Function updates the remote community_managers table with data from the monthly pdf download.

    :param file: management csv
    """
    logger.info(f"updating remote table: {MANAGEMENT_TABLE}")

    with Session(remote_engine) as remote_session:
        for manager in community_managers:
            m_id, community, situs, city, ph, email, mgr = manager
            m_id: int = int(m_id) + 1

            item = SCHEMA_CM(
                COMMUNITY=community,
                BOARD_SITUS=situs,
                BOARD_CITY=city,
                MANAGER=mgr,
                CONTACT_ADX=email,
                CONTACT_PH=ph,
            )
            db_item = MODEL_CM(**item.model_dump())

            try:
                update_statement: Update = (
                    update(MODEL_CM)
                    .where(MODEL_CM.ID == m_id)
                    .values(
                        ID=m_id,
                        BOARD_SITUS=db_item.BOARD_SITUS,
                        BOARD_CITY=db_item.BOARD_CITY,
                        MANAGER=db_item.MANAGER,
                        CONTACT_ADX=db_item.CONTACT_ADX,
                        CONTACT_PH=db_item.CONTACT_PH,
                    )
                )

                remote_session.execute(update_statement)
                remote_session.commit()

            except exc.OperationalError as e:
                logger.error(e)

    logger.info(f"updated remote table: {MANAGEMENT_TABLE}")


def update_managers(managers_file: Path) -> None:
    """
    Function updates the community_managers tables (local, remote) with data from the monthly pdf download.

    :param file: management csv
    """
    logger.info("STARTED: DATABASE TABLE UPDATES")

    community_managers: list[str] = get_communities(managers_file)
    update_local_table(community_managers)
    update_remote_table(community_managers)

    logger.info("COMPLETED: DATABASE TABLE UPDATES")


if __name__ == "__main__":
    CSV_PATH: Path = Path.cwd().parent / "output" / "csv"
    CSV_FILENAME: str = "surpriseaz-hoa-management.csv"
    PDF_NEW_FILENAME: str = "MANAGEMENT.pdf"
    PDF_PATH: Path = Path.cwd() / "output" / "pdf"
    update_managers(CSV_PATH / CSV_FILENAME)

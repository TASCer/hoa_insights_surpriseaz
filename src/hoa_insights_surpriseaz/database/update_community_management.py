import csv
import os
import logging

from logging import Logger
from sqlalchemy.orm import Session
from sqlalchemy import Engine, create_engine, exc, TextClause, text
from hoa_insights_surpriseaz.database.models_local import CommunityManagement as DBCM
from hoa_insights_surpriseaz.schemas import CommunityManagement as SCM
from hoa_insights_surpriseaz import my_secrets

LOCAL_DB_URI: str = f"{my_secrets.prod_debian_uri}"
REMOTE_DB_URI: str = f"{my_secrets.prod_bluehost_uri}"

logger: Logger = logging.getLogger(__name__)

MANAGEMENT_TABLE: str = "community_managers"


def get_pdf_communities(parsed_pdf: str) -> list[str]:
    """
    Function takes in the path of the management pdf file that was downloaded and parsed to csv.
    Reads the file and creates a row for each community and drops the header.
    Returns list of str.
    """

    try:
        with open(parsed_pdf, "r") as f:
            reader = csv.reader(f)
            pdf_communitities: list = [f for f in reader]
            pdf_communitities.pop(0)

            return pdf_communitities

    except FileNotFoundError as ffe:
        logger.addFilter(f"{ffe}")


def update() -> None:
    """
    Function updates the community_managers tables (local, remote) with data from the monthly pdf download.
    """
    pdf_managers: list = get_pdf_communities(
        os.path.abspath("./output/csv/surpriseaz-hoa-management.csv")
    )

    local_engine: Engine = create_engine(f"mysql+pymysql://{LOCAL_DB_URI}", echo=False)

    with Session(local_engine) as ls:
        for pdf_item in pdf_managers:
            id, community, situs, city, ph, email, mgr = pdf_item
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
                insert_qry: TextClause = f"""UPDATE hoa_surpriseaz.{MANAGEMENT_TABLE} 
                SET BOARD_SITUS='{db_item.BOARD_SITUS}', BOARD_CITY='{db_item.BOARD_CITY}', MANAGER='{db_item.MANAGER}', CONTACT_ADX='{db_item.CONTACT_ADX}', CONTACT_PH='{db_item.CONTACT_PH}'
                WHERE ID = '{db_item.ID}'
                    ;"""

                ls.execute(text(insert_qry))
                ls.commit()

            except exc.OperationalError as e:
                logger.error(e)

    # TODO REMOTE ISSUES VERIFY MAR RUN
    remote_engine: Engine = create_engine(
        f"mysql+pymysql://{REMOTE_DB_URI}", echo=False
    )

    with Session(remote_engine) as rs:
        for pdf_item in pdf_managers:
            id, community, situs, city, ph, email, mgr = pdf_item
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
                insert_qry: TextClause = f"""UPDATE tascsnet_hoa_surpriseaz.{MANAGEMENT_TABLE} 
                SET BOARD_SITUS='{db_item.BOARD_SITUS}', BOARD_CITY='{db_item.BOARD_CITY}', MANAGER='{db_item.MANAGER}', CONTACT_ADX='{db_item.CONTACT_ADX}', CONTACT_PH='{db_item.CONTACT_PH}'
                WHERE COMMUNITY = '{db_item.ID}'
                    ;"""

                rs.execute(text(insert_qry))
                rs.commit()

            except exc.OperationalError as e:
                logger.error(e)


if __name__ == "__main__":
    # print(update())
    csv_filename: str = "./output/csv/surpriseaz-hoa-management.csv"
    print(get_pdf_communities(csv_filename))

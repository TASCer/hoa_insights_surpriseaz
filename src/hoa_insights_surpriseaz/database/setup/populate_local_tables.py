import csv
import logging

from logging import Logger
from hoa_insights_surpriseaz.schemas import CommunityManagement, Community, Parcels
from hoa_insights_surpriseaz.database import models_local
from hoa_insights_surpriseaz.utils.file_renamer import rename
from hoa_insights_surpriseaz import my_secrets
from hoa_insights_surpriseaz import convert_management_data
from hoa_insights_surpriseaz.fetch_community_management import download

from pathlib import Path
from sqlalchemy import Engine, create_engine, exc, TextClause
from sqlalchemy import text
from sqlalchemy.orm import Session
from hoa_insights_surpriseaz.database.update_community_management import (
    get_communities,
)

PDF_DOWNLOADED_FILENAME: str = "HOA Contact List (PDF) .pdf"
PDF_NEW_FILENAME: str = "MANAGEMENT.pdf"
PDF_PATH: Path = Path.cwd().parent.parent / "output" / "pdf"

LOCAL_DB_URI: str = f"{my_secrets.prod_local_uri}"
MANAGEMENT_FILE: Path = (
    Path.cwd().parent.parent / "output" / "csv" / "surpriseaz-hoa-management.csv"
)
PARCELS_SEED_FILE: Path = Path.cwd() / "seed_data" / "parcel_constants.csv"

PARCELS_TABLE: str = "parcels"
COMMUNITY_TABLE: str = "communitites"

logger: Logger = logging.getLogger(__name__)


management_ids: list = [
    1,
    4,
    5,
    10,
    11,
    13,
    15,
    18,
    20,
    19,
    30,
    31,
    26,
    36,
    38,
    41,
    45,
    64,
    63,
    73,
    74,
]


def community_management(db: Session, management_file: Path = MANAGEMENT_FILE) -> bool:
    """
    Function checks if the HOA management csv file exists.
    If not found, download the pdf, rename and convert to csv.
    If found, read file and update database with data.

    :param db: database session
    :param management_file: path to management file, defaults to MANAGEMENT_FILE
    :return: True if exists or created
    """
    if not management_file:
        logger.warning(f"{management_file.name} not found.")
        print(f"{management_file.name} not found.")

        try:
            logger.info("Fetching Community Management Data")
            print("Fetching Community Management Data")

            download()
            file_renamed: bool = rename(
                old=PDF_PATH / PDF_DOWNLOADED_FILENAME, new=PDF_PATH / PDF_NEW_FILENAME
            )
            if file_renamed:
                convert_management_data.pdf_to_csv(
                    pdf_file=PDF_PATH / PDF_DOWNLOADED_FILENAME,
                    csv_file=MANAGEMENT_FILE,
                )
            community_management(db=db)

        except FileNotFoundError as ffe:
            logger.error(ffe)

    else:
        logger.info(f"** {management_file.name} found. **")
        print(f"{management_file.name} found.")
        management: list = get_communities(management_file)

        for manager in management:
            _, community, situs, city, ph, email, mgr = manager
            item = CommunityManagement(
                COMMUNITY=community,
                BOARD_SITUS=situs,
                BOARD_CITY=city,
                MANAGER=mgr,
                CONTACT_ADX=email,
                CONTACT_PH=ph,
            )
            db_item = models_local.CommunityManagement(**item.model_dump())

            db.add(db_item, _warn=False)
            db.commit()

    return True


def communities(db: Session, file_path=MANAGEMENT_FILE) -> list:
    """
    Function creates a table of community totals from the parcels table.
    Calls community_management function with list of community totals to populate community_managers table.

    :param db: database session
    :param file_path: HOA management file, defaults to MANAGEMENT_FILE
    :return: sequence of community totals with management id
    """
    ix = 0
    with db as session:
        community_instances: list = []

        try:
            q_community_totals: TextClause = session.execute(
                text(
                    f"SELECT COMMUNITY, count(COMMUNITY) as COUNT, avg(`LONG`) as `LONG`, avg(LAT) as LAT FROM {PARCELS_TABLE} group by COMMUNITY order by COMMUNITY;"
                )
            )
            community_totals: list = [x for x in q_community_totals]

        except exc.SQLAlchemyError as sa_err:
            logger.error(sa_err)
            print(sa_err)

        for community, parcel_total, long, lat in community_totals:
            community_schema = Community(
                COMMUNITY=community,
                LAT=lat,
                LONG=long,
                COUNT=parcel_total,
                MANAGED_ID=management_ids[ix],
            )
            community_instance = models_local.Community(**community_schema.model_dump())
            community_instances.append(community_instance)
            ix += 1
            session.add(community_instance, _warn=False)
            session.commit()

    community_management(session, file_path)

    return community_totals


def parcels(db: Session, file=f"{PARCELS_SEED_FILE}") -> bool:
    """
    Function populates the parcels table from file.
    Returns True/False depending on if successful.

    :param db: _description_
    :param file: parcels seed data, defaults to f"{PARCELS_SEED_FILE}"
    :return: True if parcels table populated
    """
    with db as session:
        parcel_instances: list = []

        try:
            with open(file) as f:
                reader = csv.reader(f)
                next(reader)
                for parcel in reader:
                    APN, COMMUNITY, SITUS, LAT, LONG = parcel[0:5]
                    parcel_instance = Parcels(
                        APN=APN, COMMUNITY=COMMUNITY, SITUS=SITUS, LAT=LAT, LONG=LONG
                    )
                    db_parcel_instance = models_local.Parcel(
                        **parcel_instance.model_dump()
                    )
                    parcel_instances.append(db_parcel_instance)
                session.add_all(parcel_instances)
                session.commit()

        except IOError as e:
            print(e)
            return False

    return True


if __name__ == "__main__":
    engine: Engine = create_engine(f"mysql+pymysql://{LOCAL_DB_URI}", echo=False)
    session = Session(bind=engine)  # parcels()
    print(communities(session))

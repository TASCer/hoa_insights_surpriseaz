import csv
import logging


from hoa_insights_surpriseaz import my_secrets
from hoa_insights_surpriseaz import convert_management_data
from hoa_insights_surpriseaz.database import models_local
from hoa_insights_surpriseaz.database.update_community_management import (
    get_managed_communities,
)
from hoa_insights_surpriseaz.fetch_community_management import download
from hoa_insights_surpriseaz.schemas import CommunityManagement, Community, Parcels
from hoa_insights_surpriseaz.utils.file_renamer import rename
from logging import Logger
from pathlib import Path
from sqlalchemy import exc, select, Result
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

PDF_DOWNLOADED_FILENAME: str = "HOA Contact List (PDF) .pdf"
PDF_NEW_FILENAME: str = "MANAGEMENT.pdf"
PDF_PATH: Path = Path.cwd().parent.parent / "output" / "pdf"

LOCAL_DB_URI: str = f"{my_secrets.prod_local_uri}"
MANAGEMENT_FILE: Path = Path.cwd() / "seed_data" / "surpriseaz-hoa-management.csv"
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


def community_management(db: Session) -> bool:
    """
    Function populates the community_managers local database table.

    :param db: database session
    :param management_file: parsed management file, defaults to MANAGEMENT_FILE
    :return: True if table populated
    """
    if not MANAGEMENT_FILE:
        logger.warning(f"{MANAGEMENT_FILE.name} not found.")
        print(f""" "{MANAGEMENT_FILE.name}" not found.""")

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
        logger.info(f"{MANAGEMENT_FILE.name} found.")
        print(f""" "{MANAGEMENT_FILE.name}" found in {MANAGEMENT_FILE.parent.resolve()}.""")
        area_hoa_managers: list = get_managed_communities(MANAGEMENT_FILE)
        for manager in area_hoa_managers:
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

    logger.info(f"\t{len((area_hoa_managers))=}")

    return True


def communities(db: Session) -> list[models_local.Community]:
    """
    Function populates communities table,

    :param db: database session
    :param file_path: parsed management file, defaults to MANAGEMENT_FILE
    :return: sequence Community instances
    """
    ix = 0
    with db as session:
        community_instances: list = []

        try:
            q_community_totals: Result[tuple[str, int, float, float]] = session.execute(
                select(
                    models_local.Parcel.COMMUNITY,
                    func.count(models_local.Parcel.COMMUNITY).label("COUNT"),
                    func.avg(models_local.Parcel.LONG).label("LONG"),
                    func.avg(models_local.Parcel.LAT).label("LAT"),
                )
                .group_by(models_local.Parcel.COMMUNITY)
                .order_by(models_local.Parcel.COMMUNITY)
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

    return community_instances


def parcels(db: Session, file=f"{PARCELS_SEED_FILE}") -> bool:
    """
    Function populates local parcels table

    :param db: database session
    :param file: parcel constants file, defaults to f"{PARCELS_SEED_FILE}"
    :return: True if table populated
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

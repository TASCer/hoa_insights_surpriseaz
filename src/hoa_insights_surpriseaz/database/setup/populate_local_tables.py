import csv
import logging

from logging import Logger
from hoa_insights_surpriseaz.schemas import CommunityManagement, Community, Parcels
from pathlib import Path
from sqlalchemy import Engine, create_engine, exc, TextClause
from sqlalchemy import text
from sqlalchemy.orm import Session
from hoa_insights_surpriseaz.database.update_community_management import (
    get_communities,
)
from hoa_insights_surpriseaz.utils.rename_files import rename
from hoa_insights_surpriseaz.database import models_local
from hoa_insights_surpriseaz import my_secrets
from hoa_insights_surpriseaz import convert_management_data
from hoa_insights_surpriseaz.fetch_community_management import download

LOCAL_DB_URI: str = f"{my_secrets.prod_debian_uri}"
MANAGEMENT_FILE: Path = (
    Path.cwd().parent.parent / "output" / "csv" / "surpriseaz-hoa-management.csv"
)
PARCELS_SEED_FILE: Path = Path.cwd() / "seed_data" / "parcel_constants.csv"

PARCELS_TABLE: str = "parcels"
COMMUNITY_TABLE: str = "communitites"

logger: Logger = logging.getLogger(__name__)

engine: Engine = create_engine(f"mysql+pymysql://{LOCAL_DB_URI}", echo=False)

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


def community_management(s: Session) -> bool:
    """
    Function takes a database session and checks if management csv file exists.
    If not found, download the pdf, rename and convert to csv.
    If found, read file and update database with data.
    """
    if not MANAGEMENT_FILE:
        logger.warning(f"{MANAGEMENT_FILE.name} not found.")
        try:
            logger.info("Fetching Community Management Data")
            download()
            file_renamed: bool = rename()
            if file_renamed:
                convert_management_data.convert_pdf()
            community_management(s=s)

        except FileNotFoundError as ffe:
            logger.error(ffe)

    else:
        logger.info(f"** {MANAGEMENT_FILE.name} found. **")
        management: list = get_communities(MANAGEMENT_FILE)

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

            s.add(db_item, _warn=False)
            s.commit()

    return True


def communities(engine: Engine = engine, file_path=MANAGEMENT_FILE) -> list:
    """
    Function creates a table of communities from parcel table data.
    """
    ix = 0
    with Session(engine) as s:
        community_instances: list = []

        try:
            q_community_totals: TextClause = s.execute(
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
            s.add(community_instance, _warn=False)
            s.commit()

    community_management(s, file_path=file_path)

    return community_totals


def parcels(file_path: str = f"{PARCELS_SEED_FILE}", engine: Engine = engine) -> bool:
    with Session(engine) as s:
        parcel_instances: list = []

        try:
            with open(file_path) as f:
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
                s.add_all(parcel_instances)
                s.commit()

        except IOError as e:
            print(e)
            return False

    return True


if __name__ == "__main__":
    parcels()

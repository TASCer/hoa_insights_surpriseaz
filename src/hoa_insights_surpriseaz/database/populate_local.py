import csv
import logging
import os

from logging import Logger
from hoa_insights_surpriseaz.schemas import CommunityManagement, Community, Parcels
from sqlalchemy import create_engine, exc, TextClause
from sqlalchemy import text
from sqlalchemy.orm import Session
from hoa_insights_surpriseaz.update_management import get_pdf_communities
from hoa_insights_surpriseaz.utils.rename_files import rename_file
from hoa_insights_surpriseaz.database import models
from hoa_insights_surpriseaz import my_secrets
from hoa_insights_surpriseaz import parse_management_pdf
from hoa_insights_surpriseaz.fetch_management_pdf import pdf_download

LOCAL_DB_URI = f"{my_secrets.prod_debian_uri}"

PARCELS_TABLE = "parcels"
COMMUNITY_TABLE = "communitites"

logger: Logger = logging.getLogger(__name__)

engine = create_engine(f"mysql+pymysql://{LOCAL_DB_URI}", echo=False)

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
    if not os.path.exists("../output/csv/surpriseaz-hoa-management.csv"):
        print("Management csv not found")
        try:
            logger.info("Management Data Not Found. Downloading/Processing PDF")
            pdf_download()
            file_renamed: bool = rename_file()
            if file_renamed:
                parse_management_pdf.convert_pdf()
            community_management(s=s)

        except FileNotFoundError as ffe:
            logger.error(ffe)

    else:
        print("management file found")
        pdf_managers = get_pdf_communities(
            os.path.abspath("../output/csv/surpriseaz-hoa-management.csv")
        )

        for pdf_item in pdf_managers:
            _, community, situs, city, ph, email, mgr = pdf_item
            item = CommunityManagement(
                COMMUNITY=community,
                BOARD_SITUS=situs,
                BOARD_CITY=city,
                MANAGER=mgr,
                CONTACT_ADX=email,
                CONTACT_PH=ph,
            )
            db_item = models.CommunityManagement(**item.model_dump())

            s.add(db_item, _warn=False)
            s.commit()

    return True


def communities() -> list:
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
            community_instance = models.Community(**community_schema.model_dump())
            community_instances.append(community_instance)
            ix += 1
            s.add(community_instance, _warn=False)
            s.commit()

    community_management(s)

    return community_totals


def parcels():
    with Session(engine) as s:
        parcel_instances: list = []

        try:
            with open(f"./seed_data/parcels.csv") as f:
                reader = csv.reader(f)
                next(reader)
                for parcel in reader:
                    print(parcel)
                    APN, COMMUNITY, SITUS, LAT, LONG = parcel[0:5]
                    parcel_instance = Parcels(
                        APN=APN, COMMUNITY=COMMUNITY, SITUS=SITUS, LAT=LAT, LONG=LONG
                    )
                    db_parcel_instance = models.Parcel(**parcel_instance.model_dump())
                    parcel_instances.append(db_parcel_instance)
                s.add_all(parcel_instances)
                s.commit()

        except IOError as e:
            print(e)
            return False

    return True


if __name__ == "__main__":
    parcels()

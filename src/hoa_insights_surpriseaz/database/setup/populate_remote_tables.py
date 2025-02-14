import logging

from logging import Logger
from sqlalchemy import create_engine, exc
from sqlalchemy import text, TextClause
from sqlalchemy.orm import Session
from hoa_insights_surpriseaz.database import local_models
from hoa_insights_surpriseaz import my_secrets
from hoa_insights_surpriseaz.schemas import Community

REMOTE_DB_URI: str = f"{my_secrets.prod_bluehost_uri}"
LOCAL_DB_URI: str = f"{my_secrets.prod_debian_uri}"

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

local_engine = create_engine(f"mysql+pymysql://{LOCAL_DB_URI}", echo=False)
bluehost_engine = create_engine(f"mysql+pymysql://{REMOTE_DB_URI}", echo=False)


def communities(community_totals) -> bool:
    """ """
    ix: int = 0
    try:
        with Session(local_engine) as ls:
            q_community_managers: TextClause = ls.execute(
                text("SELECT * from community_managers;")
            ).fetchall()
            community_managers: list = [m for m in q_community_managers]

        with Session(bluehost_engine) as rs:
            for community, parcel_total, long, lat in community_totals:
                community_instance: Community = local_models.Community(
                    COMMUNITY=community,
                    COUNT=parcel_total,
                    LAT=lat,
                    LONG=long,
                    MANAGED_ID=management_ids[ix],
                )
                rs.add(community_instance, _warn=False)
                rs.commit()
                ix += 1

            for item in community_managers:
                _, community, situs, city, mgr, email, ph = item
                db_item = local_models.CommunityManagement(
                    COMMUNITY=community,
                    BOARD_SITUS=situs,
                    BOARD_CITY=city,
                    MANAGER=mgr,
                    CONTACT_ADX=email,
                    CONTACT_PH=ph,
                )

                rs.add(db_item, _warn=False)
                rs.commit()

    except (exc.OperationalError, ValueError) as err:
        logger.error(err._message())
        return False

    return True


if __name__ == "__main__":
    communities()

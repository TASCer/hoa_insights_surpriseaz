import logging

from logging import Logger
from sqlalchemy import create_engine, Engine, exc, select
from sqlalchemy.orm import Session
from hoa_insights_surpriseaz.database.models_remote import (
    Community,
    CommunityManagement,
)
from hoa_insights_surpriseaz import my_secrets

REMOTE_DB_URI: str = f"{my_secrets.test_remote_uri}"
LOCAL_DB_URI: str = f"{my_secrets.prod_local_uri}"

LOCAL_ENGINE: Engine = create_engine(f"mysql+pymysql://{LOCAL_DB_URI}", echo=False)
REMOTE_ENGINE: Engine = create_engine(f"mysql+pymysql://{REMOTE_DB_URI}", echo=False)

REMOTE_SESSION: Session = Session(REMOTE_ENGINE)
LOCAL_SESSION = Session(LOCAL_ENGINE)

logger: Logger = logging.getLogger(__name__)


def get_local_data(local_db: Session = LOCAL_SESSION):
    """
    Function retrieves local databse table data for use in populating remote database tables.

    :param local_db: database session, defaults to LOCAL_SESSION
    :return: sequence of Community and CommunityManagement instances 
    """    
    try:
        with local_db as local_session:
            q_communities = local_session.scalars(select(Community)).all()
            q_community_management = local_session.scalars(
                select(CommunityManagement)
            ).all()

    except (exc.OperationalError, ValueError) as err:
        logger.error(err)
        return False

    return q_communities, q_community_management


def community_management(community_management_items, remote_session=REMOTE_SESSION):
    try:
        with remote_session:
            for manager in community_management_items:
                add_community_manager = CommunityManagement()
                add_community_manager.ID = manager.ID
                add_community_manager.COMMUNITY = manager.COMMUNITY
                add_community_manager.BOARD_SITUS = manager.BOARD_SITUS
                add_community_manager.BOARD_CITY = manager.BOARD_CITY
                add_community_manager.MANAGER = manager.MANAGER
                add_community_manager.CONTACT_ADX = manager.CONTACT_ADX
                add_community_manager.CONTACT_PH = manager.CONTACT_ADX

                remote_session.add(add_community_manager, _warn=False)
                remote_session.commit()

    except (exc.OperationalError, ValueError) as err:
        logger.error(err)
        return False


def communities(remote_db: Session = REMOTE_SESSION) -> list[CommunityManagement]:
    """
    Function populates remote database table communities.

    :param remote_db: database session, defaults to REMOTE_SESSION
    :return: sequence of community managers
    """
    local_community_items, local_community_managers = get_local_data()
    try:
        with remote_db as remote_session:
            for community in local_community_items:
                add_community = Community()
                add_community.COMMUNITY = community.COMMUNITY
                add_community.COUNT = community.COUNT
                add_community.LAT = community.LAT
                add_community.LONG = community.LONG
                add_community.MANAGED_ID = community.MANAGED_ID
                remote_session.add(add_community, _warn=True)
                remote_session.commit()

    except (exc.OperationalError, ValueError) as err:
        logger.error(err)

    return local_community_managers


if __name__ == "__main__":
    pass
    # communities(needed)

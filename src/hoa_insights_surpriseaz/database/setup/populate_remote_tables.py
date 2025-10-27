import logging

from logging import Logger
from sqlalchemy import create_engine, Engine, exc
from sqlalchemy import text, TextClause
from sqlalchemy.orm import Session
from hoa_insights_surpriseaz.database import models_remote
from hoa_insights_surpriseaz import my_secrets
# from hoa_insights_surpriseaz.schemas import Community

REMOTE_DB_URI: str = f"{my_secrets.test_remote_uri}"
LOCAL_DB_URI: str = f"{my_secrets.prod_local_uri}"

LOCAL_ENGINE: Engine = create_engine(f"mysql+pymysql://{LOCAL_DB_URI}", echo=False)
REMOTE_ENGINE: Engine = create_engine(f"mysql+pymysql://{REMOTE_DB_URI}", echo=False)

REMOTE_SESSION: Session = Session(REMOTE_ENGINE)
LOCAL_SESSION = Session(LOCAL_ENGINE)

logger: Logger = logging.getLogger(__name__)


def get_local_data(local_db: Session = LOCAL_SESSION):
    community_instamces = []
    community_manager_instances = []

    try:
        with local_db as local_session:
            q_communities: TextClause = local_session.execute(text("SELECT * from communities;")).fetchall()
            communities: list[str] = [c for c in q_communities]

            q_community_management = local_session.execute(
                text("SELECT * from community_managers;")).fetchall()
            community_managers = [m for m in q_community_management]


    except (exc.OperationalError, ValueError) as err:
        logger.error(err)
        return False

    for community in communities:
        community_instamce = models_remote.Community()
        community_instamce.COMMUNITY = community[0]
        community_instamce.COUNT = community[1]
        community_instamce.LAT = community[2]
        community_instamce.LONG = community[3]
        community_instamce.MANAGED_ID = community[4]
        
        community_instamces.append(community_instamce)

    for manager in community_managers:
        community_manager_instance = models_remote.CommunityManagement()
        community_manager_instance.ID = manager[0]
        community_manager_instance.COMMUNITY = manager[1]
        community_manager_instance.BOARD_SITUS = manager[2]
        community_manager_instance.BOARD_CITY = manager[3]
        community_manager_instance.MANAGER = manager[4]
        community_manager_instance.CONTACT_ADX = manager[5]
        community_manager_instance.CONTACT_PH = manager[6]

        community_manager_instances.append(community_manager_instance)
    
    return community_instamces, community_manager_instances


def community_management(community_management_items, remote_session = REMOTE_SESSION):
    try:    
        with remote_session:
            for mgr in community_management_items:
                remote_session.add(mgr, _warn=False)
                remote_session.commit()


    except (exc.OperationalError, ValueError) as err:
        logger.error(err)
        return False


def communities(
    remote_db: Session = REMOTE_SESSION,
) -> bool:
    """
    Function takes in a list of community totals and updates remote communities and community_managers tables.
    Returns True/False depending on result.
    """
    local_community_items, local_community_managers  = get_local_data() 
    print(len(local_community_items), len(local_community_managers))
    
    try:    
        with remote_db as remote_session:
            for community in local_community_items:
                remote_session.add(community, _warn=False)
                remote_session.commit()

    except (exc.OperationalError, ValueError) as err:
        logger.error(err)
        return False

    return local_community_managers


if __name__ == "__main__":
    pass
    # communities(needed)

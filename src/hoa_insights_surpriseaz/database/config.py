import os

from dotenv import load_dotenv

from hoa_insights_surpriseaz.config import PROJECT_ROOT

load_dotenv()

PROD_LOCAL_DB_URI = f"{os.environ['PROD_LOCAL_DB_USER']}:{os.environ['PROD_LOCAL_DB_USER_PASSWORD']}@{os.environ['PROD_LOCAL_DB_HOST']}/{os.environ['PROD_LOCAL_DB_NAME']}"
PROD_REMOTE_DB_URI = f"{os.environ['PROD_REMOTE_DB_USER']}:{os.environ['PROD_REMOTE_DB_USER_PASSWORD']}@{os.environ['PROD_REMOTE_DB_HOST']}/{os.environ['PROD_REMOTE_DB_NAME']}"
PROD_LOCAL_DB_NAME: str = f"{os.environ['PROD_LOCAL_DB_NAME']}"
PROD_LOCAL_DB_USER: str = f"{os.environ['PROD_LOCAL_DB_USER']}"
PROD_LOCAL_DB_HOST = f"{os.environ['PROD_LOCAL_DB_HOST']}"
UPDATE_COMMUNITIES: str = "update_communities"
OWNERS_TABLE: str = "owners"
PARCELS_TABLE: str = "parcels"

VIEW_COMMUNITY_RENTAL_TYPES: str = "community_rental_owner_types"
VIEW_TOP_RENTAL_TYPES: str = "top_rental_ownership_type"
VIEW_TOP_REGISTERED_RENTAL_OWNERS: str = "top_registered_rental_ownership"
VIEW_TOP_CLASSED_RENTAL_OWNERS: str = "top_classed_rental_ownership"
VIEW_TOP_RENTAL_OWNERS: str = "top_rental_ownership"
VIEW_REGISTERED_RENTALS: str = "registered_rentals"
VIEW_CLASSED_RENTALS: str = "classed_rentals"
VIEW_RENTAL_CONTACTS: str = "rental_contacts"
VIEW_COMMUNITY_SALES: str = "community_sales"
VIEW_PARCEL_OWNER_HISTORY = "parcel_historical_ownership"
RENTALS_TABLE: str = "rentals"
COMMUNITY_TABLE: str = "communities"

DB_INIT_LOG_NAME = "__database-setup__log"
DB_INIT_LOG = PROJECT_ROOT / "database" / "setup" / DB_INIT_LOG_NAME

# TODO REDO this
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

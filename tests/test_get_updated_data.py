# TODO data not there? timing? do a refresh?
import os
from dotenv import load_dotenv
from hoa_insights_surpriseaz.database import get_updated_parcels

load_dotenv()


def test_get_updates_db() -> None:
    owners, sales = get_updated_parcels.changes(os.environ["TEST_LOCAL_DB_URI"])
    print("OWNERS", owners)
    print("SALES", sales)

    if owners:
        assert len(owners) == 4
    if sales:
        assert len(sales) == 2

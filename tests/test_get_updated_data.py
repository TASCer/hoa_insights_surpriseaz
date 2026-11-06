# TODO data not there? timing? do a refresh?
import os

from dotenv import load_dotenv

from hoa_insights_surpriseaz.database import get_updated_parcels

load_dotenv()


def test_get_updates_db() -> None:
    new_owners, old_owners, new_sales, old_sales = get_updated_parcels.changes(os.environ["TEST_LOCAL_DB_URI"])
    print("OWNERS", new_owners)
    print("SALES", new_sales)

    assert len(new_owners) == 4
    assert len(new_sales) == 2
    assert len(old_owners) == 4
    assert len(old_sales) == 2

# TODO data not there? timing? do a refresh?
import pytest
from dotenv import load_dotenv

from conftest import TEST_LOCAL_DB_URI
from hoa_insights_surpriseaz.database import get_updated_parcels

load_dotenv()


@pytest.mark.order(-1)
def test_get_updates_db() -> None:
    new_owners, old_owners, new_sales, old_sales = get_updated_parcels.changes(
        TEST_LOCAL_DB_URI
    )
    print("OWNERS", new_owners[0][0])
    print("SALES", new_sales[0][0])

    assert len(new_owners) == 3
    assert len(new_sales) == 5
    assert len(old_owners) == 3
    assert len(old_sales) == 5

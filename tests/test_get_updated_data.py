# TODO data not there? timing? do a refresh?
from hoa_insights_surpriseaz.database import get_updated_parcels
from hoa_insights_surpriseaz.my_secrets import test_local_uri


def test_get_updates_db() -> None:
    owners, sales = get_updated_parcels.changes(test_local_uri)
    print("OWNERS", owners)
    print("SALES", sales)

    if owners:
        assert len(owners) == 4
    if sales:
        assert len(sales) == 2

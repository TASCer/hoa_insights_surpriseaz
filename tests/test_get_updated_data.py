from hoa_insights_surpriseaz.database import get_updated_data
from hoa_insights_surpriseaz.my_secrets import test_debian_uri


def test_get_updates_db():
    owners, sales = get_updated_data.changes(test_debian_uri)
    print("OWNERS", owners)
    print("SALES", sales)

    if owners:
        assert len(owners) == 4
    if sales:
        assert len(sales) == 2

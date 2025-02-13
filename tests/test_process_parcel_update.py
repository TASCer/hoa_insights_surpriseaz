# from sqlalchemy import text

from hoa_insights_surpriseaz.database import update_local_tables
from hoa_insights_surpriseaz.my_secrets import test_debian_uri, test_debian_dbname


def test_update_owner_data(parse_owner_update_data) -> list[dict]:
    update_owners, update_rentals = parse_owner_update_data
    assert len(parse_owner_update_data) == 2

    updated_owners = [x for x in update_owners if x.APN == "509-11-455"]

    assert updated_owners[0].OWNER == "BUYER NEW A"

    assert len(update_rentals) == 1

    # assert update_rentals[0].OWNER == "RENTAL NEW A"

    update_local_tables.owners(
        update_owners, db_name=test_debian_dbname, db_uri=test_debian_uri
    )
    update_local_tables.rentals(
        update_rentals, db_name=test_debian_dbname, db_uri=test_debian_uri
    )


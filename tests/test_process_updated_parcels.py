# from sqlalchemy import text

from hoa_insights_surpriseaz.database import update_local_tables
from hoa_insights_surpriseaz.my_secrets import test_debian_uri, test_debian_dbname


def test_initial_parcel_data(parse_owner_seed_data) -> list[dict]:
    initial_parcels, initial_rentals = parse_owner_seed_data
    assert len(parse_owner_seed_data) == 2
    assert len(initial_parcels) == 5

    initial_owner_check = [x for x in initial_parcels if x.APN == "509-11-455"]

    assert initial_owner_check[0].OWNER == "STEVENS TODD"

    assert len(initial_rentals) == 2

    update_local_tables.owners(
        initial_parcels, db_name=test_debian_dbname, db_uri=test_debian_uri
    )
    update_local_tables.rentals(
        initial_rentals, db_name=test_debian_dbname, db_uri=test_debian_uri
    )


def test_update_parcel_data(parse_owner_update_data) -> list[dict]:
    update_owners, update_rentals = parse_owner_update_data
    assert len(parse_owner_update_data) == 2

    updated_owners = [x for x in update_owners if x.APN == "509-11-455"]

    assert updated_owners[0].OWNER == "BUYER NEW A"

    assert len(update_rentals) == 2

    # assert update_rentals[0].OWNER == "RENTAL NEW A"

    update_local_tables.owners(
        update_owners, db_name=test_debian_dbname, db_uri=test_debian_uri
    )
    update_local_tables.rentals(
        update_rentals, db_name=test_debian_dbname, db_uri=test_debian_uri
    )

# if __name__ == "__main__":
#     updates = test_initial_parcel_data()()

# from sqlalchemy import text

from hoa_insights_surpriseaz.database import update_local_tables
from hoa_insights_surpriseaz.my_secrets import test_debian_uri, test_debian_dbname


def test_initial_parcel_data(parse_owner_seed_data) -> list[dict]:
    initial_parcels, initial_rentals = parse_owner_seed_data
    assert len(parse_owner_seed_data) == 2
    assert len(initial_parcels) == 15

    initial_owner_check = [x for x in initial_parcels if x.APN == "509-11-455"]

    assert initial_owner_check[0].OWNER == "STEVENS TODD"

    assert len(initial_rentals) == 7

    update_local_tables.owners(
        initial_parcels, db_name=test_debian_dbname, db_uri=test_debian_uri
    )
    update_local_tables.rentals(
        initial_rentals, db_name=test_debian_dbname, db_uri=test_debian_uri
    )


# if __name__ == "__main__":
#     updates = test_initial_parcel_data()()

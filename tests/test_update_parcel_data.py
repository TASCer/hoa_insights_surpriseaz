from sqlalchemy import text

from hoa_insights_surpriseaz import update_parcel_data
from hoa_insights_surpriseaz.my_secrets import test_debian_uri, test_debian_dbname


def test_seed_owner_data(session, parse_owner_seed_data) -> list[dict]:
    seed_owners, seed_rentals = parse_owner_seed_data
    assert len(parse_owner_seed_data) == 2
    assert len(seed_owners) == 15
    # seed_owners, seed_rentals = parse_parcel_seed_data

    seed_owner_check = [x for x in seed_owners if x.APN == "509-11-455"]
    # new_owners = [x for x in update_owners if x.APN == "509-11-455"]

    assert seed_owner_check[0].OWNER == "STEVENS TODD"
    # assert seed_owner_check[0].OWNER == "BUYER NEW"

    assert len(seed_rentals) == 4
    # assert len(update_rentals) == 3
    print(test_debian_uri)
    update_parcel_data.owners(
        seed_owners, db_name=test_debian_dbname, db_uri=test_debian_uri
    )


# def test_update_owner_data(session, parse_owner_update_data) -> list[dict]:
#     update_owners, update_rentals = parse_owner_update_data
#     assert len(parse_owner_update_data) == 2

#     # owners = [x for x in seed_owners if x.APN == "509-11-455"]
#     updated_owners = [x for x in update_owners if x.APN == "509-11-455"]

#     # assert owners[0].OWNER == "STEVENS TODD"
#     assert updated_owners[0].OWNER == "BUYER NEW"

#     # assert len(seed_rentals) == 4
#     assert len(update_rentals) == 3

#     update_parcel_data.owners(update_owners, db_uri=test_debian_uri)


if __name__ == "__main__":
    updates = test_seed_owner_data()
    # parsed_owner_data, parsed_rental_data = parse(updates)

from sqlalchemy import text


def test_update_parcel(connection, parse_parcel_seed_data, parse_parcel_update_data) -> list[dict]:

    # assert count == 15
    assert len(parse_parcel_seed_data) == 2
    assert len(parse_parcel_update_data) == 2
    seed_owners, seed_rentals = parse_parcel_seed_data #if x.OWNER == "Todd Stevens"]
    update_owners, update_rentals = parse_parcel_update_data #if x.OWNER == "Todd Stevens"]
    
    owners = [x for x in seed_owners if x.APN == "509-11-455"]
    new_owners = [x for x in update_owners if x.APN == "509-11-455"]
    
    assert owners[0].OWNER == "STEVENS TODD"
    assert new_owners[0].OWNER == "BUYER NEW"
    
    
    assert len(seed_rentals) == 4
    assert len(update_rentals) == 3

if __name__ == "__main__":
    updates = test_update_parcel()
    # parsed_owner_data, parsed_rental_data = parse(updates)

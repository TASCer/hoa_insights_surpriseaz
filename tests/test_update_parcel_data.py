from sqlalchemy import text


def test_update_parcel(connection, parse_parcel_seed_data, parse_parcel_update_data) -> list[dict]:

    # assert count == 15
    assert len(parse_parcel_seed_data) == 15
    assert len(parse_parcel_update_data) == 15
    seed_names = [x for x in parse_parcel_seed_data] #if x.OWNER == "Todd Stevens"]
    print(seed_names)


if __name__ == "__main__":
    updates = test_update_parcel()
    # parsed_owner_data, parsed_rental_data = parse(updates)

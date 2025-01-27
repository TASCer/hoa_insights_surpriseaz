from sqlalchemy import text


def test_update_parcel(connection, update_parcels) -> list[dict]:
    result = connection.execute(text("SELECT COUNT(*) FROM owners"))
    count = result.fetchone()[0]

    assert count == 15
    # assert len(update_parcel_data[1]) == 4

if __name__ == "__main__":
    updates = test_update_parcel()
    # parsed_owner_data, parsed_rental_data = parse(updates)

    
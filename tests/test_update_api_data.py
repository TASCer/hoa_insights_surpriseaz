def test_fetch_api(update_parcels) -> list[dict]:
    assert len(update_parcels) == 15

    # assert len(consumed_parcel_data) == 15


if __name__ == "__main__":
    print(test_fetch_api())

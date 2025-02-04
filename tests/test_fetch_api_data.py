def test_fetch_api(get_owner_seed_data) -> list[dict]:
    assert len(get_owner_seed_data) == 15

    # assert len(consumed_parcel_data) == 15


if __name__ == "__main__":
    print(test_fetch_api())

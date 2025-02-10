def test_fetch_api(get_owner_seed_data) -> list[dict]:
    assert type(get_owner_seed_data) is list
    assert len(get_owner_seed_data) == 15


if __name__ == "__main__":
    print(test_fetch_api())

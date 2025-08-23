def test_api_seed(get_owner_seed_data) -> list[dict]:
    assert type(get_owner_seed_data) is list
    assert len(get_owner_seed_data) == 15



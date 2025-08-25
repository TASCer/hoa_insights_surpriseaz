def test_api_seed(get_owner_seed_data) -> list[dict]:
    assert type(get_owner_seed_data) is list
    assert type(get_owner_seed_data[0]) is dict
    assert len(get_owner_seed_data) == 5

def test_api_update(get_owner_update_data) -> list[dict]:
    assert type(get_owner_update_data) is list
    assert type(get_owner_update_data[0]) is dict
    assert len(get_owner_update_data) == 5

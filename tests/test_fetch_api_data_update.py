def test_api_update(get_owner_update_data) -> list[dict]:
    assert type(get_owner_update_data) is list
    assert len(get_owner_update_data) == 5

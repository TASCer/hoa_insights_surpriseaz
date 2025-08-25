def test_psuedo_api_original(get_original_parcel_data) -> list[dict]:
    assert type(get_original_parcel_data) is list
    assert type(get_original_parcel_data[0]) is dict
    assert len(get_original_parcel_data) == 5


def test_psuedo_api_new(get_new_parcel_data) -> list[dict]:
    assert type(get_new_parcel_data) is list
    assert type(get_new_parcel_data[0]) is dict
    assert len(get_new_parcel_data) == 5

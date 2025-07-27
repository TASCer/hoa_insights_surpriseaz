from hoa_insights_surpriseaz import fetch_assessor_parcels


APNS = ["509-11-455", "509-11-600"]


consumed_parcel_data = fetch_assessor_parcels.parcels_api(APNS)
print(consumed_parcel_data)
# def test_api_seed(get_owner_seed_data) -> list[dict]:
#     assert type(get_owner_seed_data) is list
#     assert len(get_owner_seed_data) == 15


# def test_api_update(get_owner_update_data) -> list[dict]:
#     assert type(get_owner_update_data) is list
#     assert len(get_owner_update_data) == 2


# if __name__ == "__main__":
#     print(test_api_seed())
#     print(test_api_update())

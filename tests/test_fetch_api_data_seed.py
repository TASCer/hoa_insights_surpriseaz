def test_api_seed(get_owner_seed_data) -> list[dict]:
    assert type(get_owner_seed_data) is list
    assert len(get_owner_seed_data) == 15


# def test_api_update(get_owner_update_data) -> list[dict]:
#     assert type(get_owner_update_data) is list
#     assert len(get_owner_update_data) == 2



# if __name__ == "__main__":
#     print(test_api_seed())
#     print(test_api_update())
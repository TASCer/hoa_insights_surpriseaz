def test_init_local_db(local_session) -> None:
    assert local_session


def test_init_remote_db(remote_session):
    assert remote_session


# from hoa_insights_surpriseaz.database import get_updated_data, update_local_tables
# from hoa_insights_surpriseaz.my_secrets import test_debian_uri, test_debian_dbname


# def test_get_updates_db(local_session):
#     owners, sales = get_updated_data.changes(test_debian_uri)
#     print("OWNERS", owners)
#     assert len(owners) == 2
#     assert len(sales) == 1

#     seed_owner_check = [x for x in owners if x.APN == "509-11-455"]

#     assert seed_owner_check[0].OWNER == "STEVENS TODD"

#     assert len(sales) == 7



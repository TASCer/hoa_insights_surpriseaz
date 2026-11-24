from hoa_insights_surpriseaz.main import community_management_update


def test_get_management_update() -> None:
    data_file = community_management_update()

    assert data_file

from hoa_insights_surpriseaz.database.setup import (
    populate_remote_tables,
)


def test_populate_remote_tables(
    test_create_remote_session, test_create_local_session
) -> None:
    community_totals = populate_remote_tables.communities(
        remote_db=test_create_remote_session
    )
    assert community_totals

    management = populate_remote_tables.community_management(
        remote_db=test_create_remote_session, local_db=test_create_local_session
    )
    assert management

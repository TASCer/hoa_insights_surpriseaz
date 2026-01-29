from hoa_insights_surpriseaz.database.setup import (
    create_local_database,
    create_remote_database,

)
from pathlib import Path


def test_create_local_dbms(test_create_local_engine) -> None:
    check_local: bool = create_local_database.create(test_create_local_engine)

    assert check_local


def test_create_remote_dbms(test_create_remote_engine) -> None:
    check_remote: bool = create_remote_database.create(test_create_remote_engine)

    assert check_remote


# def test_populate_local_tables(test_create_local_session) -> None:
#     global COMMUNITY_TOTALS
#     populate_local_tables.parcels(
#         file=TEST_PARCELS_CONSTANTS, db=test_create_local_session
#     )
#     community_totals = populate_local_tables.communities(
#         db=test_create_local_session, file_path=TEST_MANAGEMENT_CSV_PATH
#     )

#     COMMUNITY_TOTALS = community_totals.copy()


# def test_populate_remote_tables(test_create_remote_session) -> None:
#     populate_remote_tables.communities(
#         remote_db=test_create_remote_session,
#     )

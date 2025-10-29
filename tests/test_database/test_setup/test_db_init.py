# from hoa_insights_surpriseaz.my_secrets import (
#     test_debian_uri,
#     test_debian_dbname,
#     test_bluehost_uri,
# )
# from hoa_insights_surpriseaz.database import (
#     models_local,
#     models_remote,
# )
from hoa_insights_surpriseaz.database.setup import (
    create_local_database,
    create_remote_database,
    populate_local_tables,
    populate_remote_tables,
)
from pathlib import Path

TEST_INITIAL_PARCELS_PATH: Path = (
    Path.cwd() / "tests" / "input" / "original_parcel_json"
)
TEST_UPDATE_PARCELS_PATH: Path = Path.cwd() / "tests" / "input" / "new_parcel_json"
# TEST_MANAGEMENT_PDF_PATH: str = "./tests/input/HOA Contact List (PDF).pdf"
TEST_MANAGEMENT_CSV_PATH: Path = (
    Path.cwd() / "tests" / "output" / "csv" / "surpriseaz-hoa-management.csv"
)
TEST_PARCELS_CONSTANTS: Path = (
    Path().cwd()
    / "tests"
    / "test_database"
    / "test_setup"
    / "test_original_data"
    / "test_parcel_constants.csv"
)
# TODO temp (copy of populate local results) fix until I refactor initial setup
COMMUNITY_TOTALS = []


def test_create_local_dbms(test_create_local_engine) -> None:
    check_local: bool = create_local_database.create(test_create_local_engine)

    assert check_local


def test_create_remote_dbms(test_create_remote_engine) -> None:
    check_remote: bool = create_remote_database.create(test_create_remote_engine)

    assert check_remote


def test_populate_local_tables(
    test_create_local_session, test_create_local_engine
) -> None:
    global COMMUNITY_TOTALS
    populate_local_tables.parcels(
        file=TEST_PARCELS_CONSTANTS, db=test_create_local_session
    )
    community_totals = populate_local_tables.communities(
        db=test_create_local_session, file_path=TEST_MANAGEMENT_CSV_PATH
    )

    COMMUNITY_TOTALS = community_totals.copy()


def test_populate_remote_tables(test_create_remote_session) -> None:
    populate_remote_tables.communities(
        remote_db=test_create_remote_session,
    )

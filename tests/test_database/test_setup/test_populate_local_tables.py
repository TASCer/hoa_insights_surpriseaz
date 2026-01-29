from hoa_insights_surpriseaz.database.setup import (
    create_local_database,
    create_remote_database,
    populate_local_tables,
    populate_remote_tables,
)
from pathlib import Path

# PARCELS_SEED_FILE: Path = Path.cwd().parent.parent / "database" / "setup" / "seed_data" / "parcel_constants.csv"

# TEST_INITIAL_PARCELS_PATH: Path = (
#     Path.cwd() / "tests" / "input" / "original_parcel_json"
# )
# TEST_UPDATE_PARCELS_PATH: Path = Path.cwd() / "tests" / "input" / "new_parcel_json"
# TEST_MANAGEMENT_CSV_PATH: Path = (
#     Path.cwd() / "tests" / "output" / "csv" / "surpriseaz-hoa-management.csv"
# )
PARCELS_CONSTANTS: Path = (
    Path.cwd()
    / "src"
    / "hoa_insights_surpriseaz"
    / "database"
    / "setup"
    / "seed_data"
    / "parcel_constants.csv"
)

# TODO temp (copy of populate local results) fix until I refactor initial setup
COMMUNITY_TOTALS = []


def test_populate_local_tables(test_create_local_session) -> None:
    parcel_totals = populate_local_tables.parcels(
        db=test_create_local_session, file=PARCELS_CONSTANTS
    )

    assert parcel_totals

    community_totals = populate_local_tables.communities(db=test_create_local_session)

    assert len(community_totals) == 21

    # COMMUNITY_TOTALS = community_totals.copy()
    assert len(community_totals) > 0

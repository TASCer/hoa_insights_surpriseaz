from hoa_insights_surpriseaz.database.setup import (
    populate_local_tables,
)
from pathlib import Path

PARCELS_CONSTANTS: Path = (
    Path.cwd()
    / "src"
    / "hoa_insights_surpriseaz"
    / "database"
    / "setup"
    / "seed_data"
    / "parcel_constants.csv"
)

MANAGEMENT_CONSTANTS: Path = (
    Path.cwd()
    / "src"
    / "hoa_insights_surpriseaz"
    / "database"
    / "setup"
    / "seed_data"
    / "surpriseaz-hoa-management.csv"
)


def test_populate_local_tables(test_create_local_session) -> None:
    parcel_totals: bool = populate_local_tables.parcels(
        db=test_create_local_session, parcel_file=PARCELS_CONSTANTS
    )

    assert parcel_totals

    community_totals = populate_local_tables.communities(db=test_create_local_session)
    assert community_totals

    management: bool = populate_local_tables.community_management(
        test_create_local_session, management_file=MANAGEMENT_CONSTANTS
    )
    assert management

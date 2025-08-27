from conftest import remote_engine
from hoa_insights_surpriseaz.database import models_local
from hoa_insights_surpriseaz.database import models_remote
from hoa_insights_surpriseaz.my_secrets import (
    test_debian_uri,
    test_debian_dbname,
    test_bluehost_dbname,
    test_bluehost_uri,
)
from hoa_insights_surpriseaz.database import (
    check_local_rdbms,
    check_remote_rdbms,
    models_local,
    models_remote,
)
from hoa_insights_surpriseaz.database.setup import (
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
COMMUNITY_TOTALS = []


def test_create_local_dbms(local_engine) -> list:
    check: bool = check_local_rdbms.schema(db_uri=test_debian_uri)

    if not check:
        print("CANNOT CONNECT CREATE TEST SCHEMA")

    models_local.Base.metadata.create_all(local_engine)


def test_create_renote_dbms(remote_engine) -> list:
    check: bool = check_local_rdbms.schema(db_uri=test_bluehost_uri)

    if not check:
        print("CANNOT CONNECT CREATE TEST SCHEMA")

    models_remote.Base.metadata.create_all(remote_engine)


def test_populate_local_tables(local_engine):
    populate_local_tables.parcels(TEST_PARCELS_CONSTANTS, engine=local_engine)
    COMMUNITY_TOTALS = populate_local_tables.communities(
        engine=local_engine, file_path=TEST_MANAGEMENT_CSV_PATH
    )
    check_local_rdbms.triggers(db_uri=test_debian_uri, db_name=test_debian_dbname)
    check_local_rdbms.views(db_uri=test_debian_uri)

    print(COMMUNITY_TOTALS)


def test_populate_remote_tables(local_engine, remote_engine):
    populate_remote_tables.communities(
        community_totals=COMMUNITY_TOTALS,
        local_db=local_engine,
        remote_db=remote_engine,
    )

    # populate_remote_tables.parcels(TEST_PARCELS_CONSTANTS, engine=local_engine)


# test_populate_remote_tables(local_engine=local_engine, remote_engine=remote_engine())

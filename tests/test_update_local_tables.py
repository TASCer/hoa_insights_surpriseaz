# from dotenv import load_dotenv

from conftest import TEST_LOCAL_DB_URI, TEST_LOCAL_ENGINE
from hoa_insights_surpriseaz.database import update_local_database

# load_dotenv()

print(TEST_LOCAL_ENGINE.url.database)


def test_update_local_tables_original(parse_original_parcel_data) -> None:
    update_local_database.owners(
        parse_original_parcel_data[0],
        db_uri=TEST_LOCAL_DB_URI,
    )
    update_local_database.rentals(
        parse_original_parcel_data[1],
        db_name=TEST_LOCAL_ENGINE.url.database,
        db_uri=TEST_LOCAL_DB_URI,
    )


def test_update_local_tables_new(parse_new_parcel_data) -> None:
    update_local_database.owners(
        parse_new_parcel_data[0],
        db_uri=TEST_LOCAL_DB_URI,
    )
    update_local_database.rentals(
        parse_new_parcel_data[1],
        db_name=TEST_LOCAL_ENGINE.url.database,
        db_uri=TEST_LOCAL_DB_URI,
    )

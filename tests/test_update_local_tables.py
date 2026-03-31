import os
from dotenv import load_dotenv
from hoa_insights_surpriseaz.database import update_local_database

load_dotenv()


def test_update_local_tables_original(parse_original_parcel_data) -> None:
    update_local_database.owners(
        parse_original_parcel_data[0],
        db_name=os.environ["TEST_LOCAL_DB_NAME"],
        db_uri=os.environ["TEST_LOCAL_DB_URI"],
    )
    update_local_database.rentals(
        parse_original_parcel_data[1],
        db_name=os.environ["TEST_LOCAL_DB_NAME"],
        db_uri=os.environ["TEST_LOCAL_DB_URI"],
    )


def test_update_local_tables_new(parse_new_parcel_data) -> None:
    update_local_database.owners(
        parse_new_parcel_data[0],
        db_name=os.environ["TEST_LOCAL_DB_NAME"],
        db_uri=os.environ["TEST_LOCAL_DB_URI"],
    )
    update_local_database.rentals(
        parse_new_parcel_data[1],
        db_name=os.environ["TEST_LOCAL_DB_NAME"],
        db_uri=os.environ["TEST_LOCAL_DB_URI"],
    )

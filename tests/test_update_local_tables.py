from hoa_insights_surpriseaz.database import update_local_tables
from hoa_insights_surpriseaz.my_secrets import test_debian_uri, test_debian_dbname


def test_update_local_tables_original(parse_original_parcel_data) -> None:
    update_local_tables.owners(
        parse_original_parcel_data[0],
        db_name=test_debian_dbname,
        db_uri=test_debian_uri,
    )
    update_local_tables.rentals(
        parse_original_parcel_data[1],
        db_name=test_debian_dbname,
        db_uri=test_debian_uri,
    )


def test_update_local_tables_new(parse_new_parcel_data) -> None:
    update_local_tables.owners(
        parse_new_parcel_data[0],
        db_name=test_debian_dbname,
        db_uri=test_debian_uri,
    )
    update_local_tables.rentals(
        parse_new_parcel_data[1],
        db_name=test_debian_dbname,
        db_uri=test_debian_uri,
    )

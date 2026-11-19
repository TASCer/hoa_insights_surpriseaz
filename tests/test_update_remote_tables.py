from conftest import TEST_LOCAL_DB_URI, TEST_REMOTE_DB_URI
from hoa_insights_surpriseaz.database import update_remote_database


def test_update_rental_tables() -> None:
    assert (
        update_remote_database.rental_tables(
            local_db=TEST_LOCAL_DB_URI,
            remote_db=TEST_REMOTE_DB_URI,
        )
        is None
    )


def test_update_financial_tables() -> None:
    assert (
        update_remote_database.financial_tables(
            local_db=TEST_LOCAL_DB_URI,
            remote_db=TEST_REMOTE_DB_URI,
        )
        is None
    )

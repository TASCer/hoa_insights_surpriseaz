import os

from hoa_insights_surpriseaz.database import update_remote_database


def test_update_rental_tables() -> None:
    assert (
        update_remote_database.rental_tables(
            local_db=os.environ["TEST_LOCAL_DB_URI"],
            remote_db=os.environ["TEST_REMOTE_DB_URI"],
        )
        is None
    )


def test_update_financial_tables() -> None:
    assert (
        update_remote_database.financial_tables(
            local_db=os.environ["TEST_LOCAL_DB_URI"],
            remote_db=os.environ["TEST_REMOTE_DB_URI"],
        )
        is None
    )

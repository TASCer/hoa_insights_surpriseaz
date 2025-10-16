from hoa_insights_surpriseaz.database import update_remote_database
from hoa_insights_surpriseaz.my_secrets import (
    test_remote_uri,
    test_local_uri,
)


def test_update_rental_tables() -> None:
    assert (
        update_remote_database.rental_tables(
            local_db=test_local_uri, remote_db=test_remote_uri
        )
        is None
    )


def test_update_financial_tables() -> None:
    assert (
        update_remote_database.financial_tables(
            local_db=test_local_uri, remote_db=test_remote_uri
        )
        is None
    )

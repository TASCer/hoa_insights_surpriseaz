from hoa_insights_surpriseaz.database.setup import (
    create_local_database,
    create_remote_database,
)


def test_create_local_dbms(test_create_local_engine) -> None:
    check_local: bool = create_local_database.create(test_create_local_engine)

    assert check_local


def test_create_remote_dbms(test_create_remote_engine) -> None:
    check_remote: bool = create_remote_database.create(test_create_remote_engine)

    assert check_remote

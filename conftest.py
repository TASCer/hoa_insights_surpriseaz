import json
import os
from pathlib import Path
import pytest

from sqlalchemy import create_engine, Engine, text
from sqlalchemy.orm import Session
from hoa_insights_surpriseaz.my_secrets import (
    test_local_uri,
    test_local_dbname,
    test_remote_uri,
    test_remote_dbname,
)

from hoa_insights_surpriseaz.parse_assessor_parcels import owner_data
from hoa_insights_surpriseaz.schemas import Owners, Rentals

TEST_INITIAL_PARCELS_PATH: Path = (
    Path.cwd() / "tests" / "input" / "original_parcel_json"
)
TEST_UPDATE_PARCELS_PATH: Path = Path.cwd() / "tests" / "input" / "new_parcel_json"
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


@pytest.fixture(scope="session")
def test_create_local_engine() -> Engine:
    test_debian_engine: Engine = create_engine(f"mysql+pymysql://{test_local_uri}")

    return test_debian_engine


@pytest.fixture(scope="session")
def test_create_local_session(test_create_local_engine):
    test_debian_session = Session(test_create_local_engine)

    try:
        yield test_debian_session

    finally:
        test_debian_session.execute(
            text(f"DROP DATABASE IF EXISTS {test_local_dbname};")
        )
        pass


@pytest.fixture(scope="session")
def test_create_remote_engine() -> Engine:
    test_bluehost_engine: Engine = create_engine(f"mysql+pymysql://{test_remote_uri}")

    return test_bluehost_engine


@pytest.fixture(scope="session")
def test_create_remote_session(test_create_remote_engine):
    test_bluehost_session = Session(test_create_remote_engine)

    try:
        yield test_bluehost_session

    finally:
        test_bluehost_session.execute(text(f"DROP DATABASE {test_remote_dbname};"))
        pass


@pytest.fixture()
def get_original_parcel_data():
    test_original_parcels: list[str] = os.listdir(f"{TEST_INITIAL_PARCELS_PATH}")

    consumed_owner_original_data: list[dict] = []

    for parcel in test_original_parcels:
        parcel_file = open(f"{TEST_INITIAL_PARCELS_PATH}/{parcel}", "r")
        parcel_data: dict = json.load(parcel_file)
        consumed_owner_original_data.append(parcel_data)

    return consumed_owner_original_data


@pytest.fixture()
def get_new_parcel_data():
    test_owner_update_data: list[str] = os.listdir(f"{TEST_UPDATE_PARCELS_PATH}")

    consumed_owner_update_data: list[dict] = []

    for parcel in test_owner_update_data:
        parcel_file = open(f"{TEST_UPDATE_PARCELS_PATH}/{parcel}", "r")
        parcel_data: dict = json.load(parcel_file)
        consumed_owner_update_data.append(parcel_data)

    return consumed_owner_update_data


@pytest.fixture()
def parse_original_parcel_data(
    get_original_parcel_data,
) -> tuple[list[Owners], list[Rentals]]:
    test_parsed_owners_original_data, test_parsed_rentals_original_data = owner_data(
        get_original_parcel_data
    )

    return test_parsed_owners_original_data, test_parsed_rentals_original_data


@pytest.fixture()
def parse_new_parcel_data(get_new_parcel_data) -> tuple[list[Owners], list[Rentals]]:
    test_parsed_new_parcel_data, test_parsed_new_rentals_data = owner_data(
        get_new_parcel_data
    )

    return test_parsed_new_parcel_data, test_parsed_new_rentals_data

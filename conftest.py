import json
import os
from pathlib import Path

import pytest
from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session

from hoa_insights_surpriseaz.parse_fetched_parcels import owners_data
from hoa_insights_surpriseaz.schemas import Owners, Rentals

load_dotenv()

TEST_INITIAL_PARCELS_PATH: Path = (
    Path.cwd() / "tests" / "input" / "original_parcel_json"
)
TEST_UPDATE_PARCELS_PATH: Path = Path.cwd() / "tests" / "input" / "new_parcel_json"
TEST_MANAGEMENT_CSV_PATH: Path = (
    Path.cwd() / "tests" / "output" / "csv" / "surpriseaz-hoa-management.csv"
)


@pytest.fixture(scope="session")
def test_create_local_engine() -> Engine:
    test_local_engine: Engine = create_engine(
        f"mysql+pymysql://{os.environ['TEST_LOCAL_DB_URI']}"
    )

    return test_local_engine


@pytest.fixture(scope="session")
def test_create_local_session(test_create_local_engine):
    test_local_session = Session(test_create_local_engine)

    try:
        yield test_local_session

    finally:
        # test_local_session.execute(
        #     text(f"DROP DATABASE IF EXISTS {os.environ['TEST_LOCAL_DB_NAME']};")
        # )
        pass


@pytest.fixture(scope="session")
def test_create_remote_engine() -> Engine:
    test_remote_engine: Engine = create_engine(
        f"mysql+pymysql://{os.environ['TEST_REMOTE_DB_URI']}"
    )

    return test_remote_engine


@pytest.fixture(scope="session")
def test_create_remote_session(test_create_remote_engine):
    test_remote_session = Session(test_create_remote_engine)

    try:
        yield test_remote_session

    finally:
        test_remote_session.execute(
            statement=text(f"DROP DATABASE {os.environ['TEST_REMOTE_DB_NAME']};")
        )
        # pass


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
    test_parsed_owners_original_data, test_parsed_rentals_original_data = owners_data(
        get_original_parcel_data
    )

    return test_parsed_owners_original_data, test_parsed_rentals_original_data


@pytest.fixture()
def parse_new_parcel_data(get_new_parcel_data) -> tuple[list[Owners], list[Rentals]]:
    test_parsed_new_parcel_data, test_parsed_new_rentals_data = owners_data(
        get_new_parcel_data
    )

    return test_parsed_new_parcel_data, test_parsed_new_rentals_data

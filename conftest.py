# https://stackoverflow.com/questions/12352455/how-to-use-sqlalchemy-to-seamlessly-access-multiple-databases
import json
import os
from pathlib import Path
import pytest

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session
from hoa_insights_surpriseaz.my_secrets import (
    test_debian_uri,
    test_bluehost_uri,
)

from hoa_insights_surpriseaz.parse_assessor_parcels import parse

# from hoa_insights_surpriseaz import process_updated_parcels
# from hoa_insights_surpriseaz.database.setup import (
#     populate_local_tables,
#     populate_remote_tables,
# )
# from hoa_insights_surpriseaz import convert_management_data

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


@pytest.fixture(scope="session")
def local_engine():
    local_engine = create_engine(f"mysql+pymysql://{test_debian_uri}")

    return local_engine


@pytest.fixture(scope="session")
def local_session(local_engine):
    local_sess = Session(local_engine)

    yield local_sess

    # local_sess.execute(text(f"DROP DATABASE {test_debian_dbname};"))


# # ISSUE POPULATING TEST BH DB
@pytest.fixture(scope="session")
def remote_engine() -> Engine:
    remote_engine = create_engine(f"mysql+pymysql://{test_bluehost_uri}")

    return remote_engine


@pytest.fixture(scope="session")
def remote_session(remote_engine):
    remote_sess = Session(remote_engine)

    yield remote_sess

    # remote_sess.execute(text(f"DROP DATABASE {test_bluehost_dbname};"))


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
def parse_original_parcel_data(get_original_parcel_data):
    test_parsed_owners_original_data, test_parsed_rentals_original_data = parse(
        get_original_parcel_data
    )

    return test_parsed_owners_original_data, test_parsed_rentals_original_data


@pytest.fixture()
def parse_new_parcel_data(get_new_parcel_data):
    test_parsed_new_parcel_data, test_parsed_new_rentals_data = parse(
        get_new_parcel_data
    )

    return test_parsed_new_parcel_data, test_parsed_new_rentals_data


# ---------------------------------

# @pytest.fixture(scope="function")
# def parse_pdf():
#     csvfile = f"{TEST_MANAGEMENT_CSV_PATH}"
#     parsed = parse_management_data.parse_csv(csvfile)
#     print(parsed)

# # return type(parsed)

# pdf = f"{TEST_MANAGEMENT_PDF_PATH}"
# converted = parse_management_pdf.convert_pdf(pdf)

# # return parsed


# @pytest.fixture(scope="function")
# def parse_pdf():
#     pdf = f"{TEST_MANAGEMENT_PDF_PATH}"
#     converted = parse_management_pdf.convert_pdf(pdf)


#     return converted

import json
import os
import pytest

from sqlalchemy import create_engine
from hoa_insights_surpriseaz.my_secrets import prod_debian_uri
from hoa_insights_surpriseaz.parse_api_data import parse
from hoa_insights_surpriseaz import update_parcel_data
from hoa_insights_surpriseaz import process_updated_parcels

TEST_SEED_FILES_PATH: str = "./tests/input/json_seed_data/"
TEST_UPDATE_FILES_PATH: str = "./tests/input/json_update_data/"


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(f"mysql+pymysql://{prod_debian_uri}")

    return engine


@pytest.fixture(scope="function")
def connection(engine):
    conn = engine.connect()
    yield conn

    conn.close()


@pytest.fixture(scope="function")
def get_seed_parcel_data():
    test_seed_parcels: list[str] = os.listdir(f"{TEST_SEED_FILES_PATH}")

    consumed_seed_data: list[dict] = []

    for parcel in test_seed_parcels:
        parcel_file = open(f"{TEST_SEED_FILES_PATH}{parcel}", "r")
        parcel_data: dict = json.load(parcel_file)
        consumed_seed_data.append(parcel_data)

    return consumed_seed_data


@pytest.fixture(scope="function")
def parse_parcel_seed_data(get_seed_parcel_data):
    test_parsed_owners_data, test_parsed_rentals_data = parse(get_seed_parcel_data)
    # test_parsed_owners_data, test_parsed_rentals_data = parse(get_update_parcel_data)
    
    return test_parsed_owners_data, test_parsed_rentals_data


@pytest.fixture(scope="function")
def get_update_parcel_data():
    test_update_parcels: list[str] = os.listdir(f"{TEST_UPDATE_FILES_PATH}")

    consumed_update_data: list[dict] = []

    for parcel in test_update_parcels:
        parcel_file = open(f"{TEST_UPDATE_FILES_PATH}{parcel}", "r")
        parcel_data: dict = json.load(parcel_file)
        consumed_update_data.append(parcel_data)

    return consumed_update_data



@pytest.fixture(scope="function")
def parse_parcel_update_data(get_update_parcel_data):
    test_parsed_owners_data, test_parsed_rentals_data = parse(get_update_parcel_data)

    return test_parsed_owners_data, test_parsed_rentals_data



# TODO need to send updates to check reports etc..


# @pytest.fixture(scope="function")
# def update_parcels(connection, parse_parcel_seed_data):
#     test_owners = update_parcel_data.owners(parse_parcel_seed_data[0])
#     test_rentals = update_parcel_data.rentals(parse_parcel_seed_data[1])

#     return test_owners, test_rentals








# @pytest.fixture(scope="function")
# def get_updates():
#     updates = process_updated_parcels.get_new_insights()

#     return updates

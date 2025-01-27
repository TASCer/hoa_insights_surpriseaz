from hoa_insights_surpriseaz import update_parcel_data
import json
import os
import pytest

from sqlalchemy import create_engine, Engine, exc, text
from hoa_insights_surpriseaz.my_secrets import debian_uri
from hoa_insights_surpriseaz.parse_api_data import parse

TEST_UPDATE_FILES_PATH: str = "./tests/input/json_seed_data/"


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(f"mysql+pymysql://{debian_uri}")

    return engine


@pytest.fixture(scope="function")
def connection(engine):
    conn = engine.connect()
    yield conn

    conn.close()

@pytest.fixture(scope="function")
def fetch_parcel_data():
    test_parcels: list[str] = os.listdir(f"{TEST_UPDATE_FILES_PATH}")
    
    consumed_parcel_data: list[dict] = []

    for parcel in test_parcels:
        parcel_file = open(f"{TEST_UPDATE_FILES_PATH}{parcel}", "r")
        parcel_data: dict = json.load(parcel_file)
        consumed_parcel_data.append(parcel_data)

    return consumed_parcel_data

@pytest.fixture(scope="function")
def parse_parcel_data(fetch_parcel_data):
    test_parsed_owners_data, test_parsed_rentals_data = parse(fetch_parcel_data)

    return test_parsed_owners_data, test_parsed_rentals_data

@pytest.fixture(scope="function")
def update_parcels(connection, parse_parcel_data):
    test_owners = update_parcel_data.owners(parse_parcel_data[0])
    test_rentals = update_parcel_data.rentals(parse_parcel_data[1])
 
 
def test_owner_count(connection):
    result = connection.execute(text("SELECT COUNT(*) FROM owners"))
    count = result.fetchone()[0]
    
    return count
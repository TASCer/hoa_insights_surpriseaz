import json
import os
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists
from hoa_insights_surpriseaz.my_secrets import test_debian_uri, prod_debian_uri
from hoa_insights_surpriseaz.parse_assessor_data import parse
from hoa_insights_surpriseaz.database import models
# from hoa_insights_surpriseaz import update_parcel_data
# from hoa_insights_surpriseaz import process_updated_parcels
from hoa_insights_surpriseaz.database import populate_local_tables
from hoa_insights_surpriseaz import parse_management_data


TEST_SEED_FILES_PATH: str = "./tests/input/json_seed_data/"
TEST_UPDATE_FILES_PATH: str = "./tests/input/json_update_data/"
TEST_MANAGEMENT_PDF_PATH: str = "./tests/input/HOA Contact List (PDF).pdf"
TEST_MANAGEMENT_CSV_PATH: str = "./tests/output/csv/surpriseaz-hoa-management.csv"
TEST_PARCELS_CONSTANTS: str = "./tests/database/test_parcel_constants.csv"


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(f"mysql+pymysql://{test_debian_uri}")
    
    if not database_exists(engine.url):
        create_database(engine.url)

    return engine


@pytest.fixture(scope="function")
def session(engine):
    sess = Session(engine)
    models.Base.metadata.create_all(engine)
    populate_local_tables.parcels(TEST_PARCELS_CONSTANTS, engine=engine)
    populate_local_tables.communities(engine=engine, file_path=TEST_MANAGEMENT_CSV_PATH)
    
    yield sess

    sess.close()

@pytest.fixture(scope="function")
def get_owner_seed_data():
    test_owner_seed_parcels: list[str] = os.listdir(f"{TEST_SEED_FILES_PATH}")

    consumed_owner_seed_data: list[dict] = []

    for parcel in test_owner_seed_parcels:
        parcel_file = open(f"{TEST_SEED_FILES_PATH}{parcel}", "r")
        parcel_data: dict = json.load(parcel_file)
        consumed_owner_seed_data.append(parcel_data)

    return consumed_owner_seed_data


@pytest.fixture(scope="function")
def parse_owner_seed_data(get_owner_seed_data):
    test_parsed_owners_seed_data, test_parsed_rentals_seed_data = parse(get_owner_seed_data)
    # test_parsed_owners_data, test_parsed_rentals_data = parse(get_update_parcel_data)

    return test_parsed_owners_seed_data, test_parsed_rentals_seed_data



@pytest.fixture(scope="function")
def get_owner_update_data():
    test_owner_update_data: list[str] = os.listdir(f"{TEST_SEED_FILES_PATH}")

    consumed_owner_update_data: list[dict] = []

    for parcel in test_owner_update_data:
        parcel_file = open(f"{TEST_SEED_FILES_PATH}{parcel}", "r")
        parcel_data: dict = json.load(parcel_file)
        consumed_owner_update_data.append(parcel_data)

    return consumed_owner_update_data

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
def parse_ownwer_update_data(get_update_parcel_data):
    test_parsed_owners_update_data, test_parsed_rentals_update_data = parse(get_update_parcel_data)

    return test_parsed_owners_update_data, test_parsed_rentals_update_data

    # @pytest.fixture(scope="function")
    # def parse_pdf():
    #     csvfile = f"{TEST_MANAGEMENT_CSV_PATH}"
    #     parsed = parse_management_data.parse_csv(csvfile)
    #     print(parsed)

    # return type(parsed)

    # pdf = f"{TEST_MANAGEMENT_PDF_PATH}"
    # converted = parse_management_pdf.convert_pdf(pdf)

    # return parsed


# @pytest.fixture(scope="function")
# def parse_pdf():
#     pdf = f"{TEST_MANAGEMENT_PDF_PATH}"
#     converted = parse_management_pdf.convert_pdf(pdf)


#     return converted



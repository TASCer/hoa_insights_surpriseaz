# https://stackoverflow.com/questions/12352455/how-to-use-sqlalchemy-to-seamlessly-access-multiple-databases
import json
import os
import pytest

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists
from hoa_insights_surpriseaz.my_secrets import (
    test_debian_uri,
    test_debian_dbname,
    test_bluehost_dbname,
    test_bluehost_uri,
)
from hoa_insights_surpriseaz.parse_assessor_parcels import parse
from hoa_insights_surpriseaz.database import (
    check_local_rdbms,
    check_remote_rdbms,
    models_local,
    models_remote,
)

# from hoa_insights_surpriseaz import update_parcel_data
# from hoa_insights_surpriseaz import process_updated_parcels
from hoa_insights_surpriseaz.database.setup import (
    populate_local_tables,
    populate_remote_tables,
)
from hoa_insights_surpriseaz import convert_management_data

INITIAL_PARCELS_PATH: str = "./tests/input/initial_parcel_json/"
UPDATE_PARCELS_PATH: str = "./tests/input/update_parcel_json/"
MANAGEMENT_PDF_PATH: str = "./tests/input/HOA Contact List (PDF).pdf"
MANAGEMENT_CSV_PATH: str = "./tests/output/csv/surpriseaz-hoa-management.csv"
PARCELS_CONSTANTS: str = (
    "./src/hoa_insights_surpriseaz/database/setup/seed_data/parcel_constants.csv"
)


@pytest.fixture(scope="session")
def local_engine():
    local_engine = create_engine(f"mysql+pymysql://{test_debian_uri}")

    if not database_exists(local_engine.url):
        create_database(local_engine.url)

    return local_engine


@pytest.fixture(scope="session")
def local_session(local_engine):
    local_sess = Session(local_engine)
    models_local.Base.metadata.create_all(local_engine)
    populate_local_tables.parcels(PARCELS_CONSTANTS, engine=local_engine)
    populate_local_tables.communities(
        engine=local_engine, file_path=MANAGEMENT_CSV_PATH
    )
    check_local_rdbms.triggers(db_uri=test_debian_uri, db_name=test_debian_dbname)
    check_local_rdbms.views(db_uri=test_debian_uri)

    yield local_sess

    # local_sess.execute(text(f"DROP DATABASE {test_debian_dbname};"))


# ISSUE POPULATING TEST BH DB
@pytest.fixture(scope="session")
def remote_engine():
    remote_engine = create_engine(f"mysql+pymysql://{test_bluehost_uri}")

    if not database_exists(remote_engine.url):
        create_database(remote_engine.url)

    return remote_engine


@pytest.fixture(scope="session")
def remote_session(remote_engine):
    remote_sess = Session(remote_engine)
    models_remote.Base.metadata.create_all(remote_engine)

    # populate_remote_tables.parcels(PARCELS_CONSTANTS, engine=local_engine)
    populate_remote_tables.communities(
        engine=remote_engine, file_path=MANAGEMENT_CSV_PATH
    )
    # check_local_rdbms.triggers(db_uri=test_debian_uri, db_name=test_debian_dbname)
    # check_local_rdbms.views(db_uri=test_debian_uri)

    yield remote_sess

    # remote_sess.execute(text(f"DROP DATABASE {test_bluehost_dbname};"))


@pytest.fixture()
def get_owner_seed_data():
    test_owner_seed_parcels: list[str] = os.listdir(f"{INITIAL_PARCELS_PATH}")

    consumed_owner_seed_data: list[dict] = []

    for parcel in test_owner_seed_parcels:
        parcel_file = open(f"{INITIAL_PARCELS_PATH}{parcel}", "r")
        parcel_data: dict = json.load(parcel_file)
        consumed_owner_seed_data.append(parcel_data)

    return consumed_owner_seed_data


@pytest.fixture()
def parse_owner_seed_data(get_owner_seed_data):
    test_parsed_owners_seed_data, test_parsed_rentals_seed_data = parse(
        get_owner_seed_data
    )

    return test_parsed_owners_seed_data, test_parsed_rentals_seed_data


@pytest.fixture()
def get_owner_update_data():
    test_owner_update_data: list[str] = os.listdir(f"{UPDATE_PARCELS_PATH}")

    consumed_owner_update_data: list[dict] = []

    for parcel in test_owner_update_data:
        parcel_file = open(f"{UPDATE_PARCELS_PATH}{parcel}", "r")
        parcel_data: dict = json.load(parcel_file)
        consumed_owner_update_data.append(parcel_data)

    return consumed_owner_update_data


@pytest.fixture()
def parse_owner_update_data(get_owner_update_data):
    test_parsed_owners_update_data, test_parsed_rentals_update_data = parse(
        get_owner_update_data
    )

    return test_parsed_owners_update_data, test_parsed_rentals_update_data


# @pytest.fixture(scope="function")
# def get_update_parcel_data():
#     test_update_parcels: list[str] = os.listdir(f"{TEST_UPDATE_FILES_PATH}")

#     consumed_update_data: list[dict] = []

#     for parcel in test_update_parcels:
#         parcel_file = open(f"{TEST_UPDATE_FILES_PATH}{parcel}", "r")
#         parcel_data: dict = json.load(parcel_file)
#         consumed_update_data.append(parcel_data)

#     return consumed_update_data


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

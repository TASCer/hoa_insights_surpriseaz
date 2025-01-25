import pytest

from sqlalchemy import create_engine, Engine, exc, text
from tests import test_database_seed
from hoa_insights_surpriseaz.my_secrets import debian_uri
from hoa_insights_surpriseaz.parse_api_data import parse
from hoa_insights_surpriseaz.update_parcel_data import owners


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
def setup_parcel_data(connection):
    test_parcel_data = test_database_seed.test_process_json()
    test_parsed_parcel_data = parse(test_parcel_data)
    
    assert len(test_parsed_parcel_data) >0

@pytest.fixture(scope="function")
def seed_parcel_data(connection):
    test_parcel_data = test_database_seed.process_json()
    test_parsed_parcel_data = parse(test_parcel_data)
    # test_owners_to_db = (test_parsed_data)

    assert len(test_parsed_parcel_data) == 15

def test_user_count(connection, setup_parcel_data):
    result = connection.execute(text("SELECT COUNT(*) FROM owners"))
    count = result.fetchone()[0]
    assert count == 0

from hoa_insights_surpriseaz import update_parcel_data
from hoa_insights_surpriseaz.schemas import Owners

# TEST_UPDATE_FILES_PATH: str = "./tests/input/json_seed_data/"


def test_parse_api(parse_parcel_data) -> list[dict]:
    parsed_test_owners, parsed_test_rentals = parse_parcel_data 
    assert len(parsed_test_owners) == 15
    assert len(parsed_test_rentals) == 4
    assert type(parsed_test_owners[0]) is Owners


if __name__ == "__main__":
    print(test_parse_api())

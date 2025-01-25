import json
import os

from hoa_insights_surpriseaz import update_parcel_data
from hoa_insights_surpriseaz.parse_api_data import parse
from hoa_insights_surpriseaz.schemas import Owners

TEST_UPDATE_FILES_PATH: str = "./tests/input/json_seed_data/"


def test_parse_api() -> list[dict]:
    test_parcels: str = os.listdir(f"{TEST_UPDATE_FILES_PATH}")
    consumed_parcel_data: list = []

    for parcel in test_parcels:
        parcel_data_file = open(f"{TEST_UPDATE_FILES_PATH}{parcel}", "r")
        parcel_data: dict = json.load(parcel_data_file)
        consumed_parcel_data.append(parcel_data)

    parsed_owner_parcels, parsed_rental_parcels = parse(consumed_parcel_data)

    assert len(parsed_owner_parcels) == 15
    assert len(parsed_rental_parcels) == 4
    assert type(parsed_owner_parcels[0]) is Owners


if __name__ == "__main__":
    print(test_parse_api())

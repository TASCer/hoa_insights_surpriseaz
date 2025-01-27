import json
import os

from hoa_insights_surpriseaz.parse_api_data import parse
from hoa_insights_surpriseaz import update_parcel_data

TEST_UPDATE_FILES_PATH: str = (
    "/home/todd/python_projects/hoa_insights_surpriseaz/tests/input/json_seed_data/"
)


def test_process_json() -> list[dict]:
    test_parcels: str = os.listdir(f"{TEST_UPDATE_FILES_PATH}")
    consumed_parcel_data: list = []

    for parcel in test_parcels:
        parcel_data_file = open(f"{TEST_UPDATE_FILES_PATH}{parcel}", "r")
        parcel_data_json = json.load(parcel_data_file)
        consumed_parcel_data.append(parcel_data_json)

    assert consumed_parcel_data


if __name__ == "__main__":
    updates = test_process_json()
    parsed_owner_data, parsed_rental_data = parse(updates)

    update_parcel_data.owners(parsed_owner_data)
    update_parcel_data.rentals(parsed_rental_data)

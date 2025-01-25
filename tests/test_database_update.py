import json
import os

from hoa_insights_surpriseaz import update_parcel_data
from hoa_insights_surpriseaz.utils.number_parser import parse_apn, parse_ph_nums
from hoa_insights_surpriseaz.utils.date_parser import api_date
from hoa_insights_surpriseaz.parse_api_data import parse

TEST_UPDATE_FILES_PATH = (
    "/home/todd/python_projects/test_hoa_surpriseaz/tests/input/json_update_data/"
)


def process_json():
    test_parcels: str = os.listdir(f"{TEST_UPDATE_FILES_PATH}")
    consumed_parcel_data = []

    for parcel in test_parcels:
        parcel_data_file = open(f"{TEST_UPDATE_FILES_PATH}{parcel}", "r")
        parcel_data_json = json.load(parcel_data_file)
        consumed_parcel_data.append(parcel_data_json)
    return consumed_parcel_data


if __name__ == "__main__":
    updates = process_json()
    parsed_owner_data, parsed_rental_data = parse(updates)

    update_parcel_data.owners(parsed_owner_data)
    update_parcel_data.rentals(parsed_rental_data)

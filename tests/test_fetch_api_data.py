import json
import os

TEST_UPDATE_FILES_PATH: str = "./tests/input/json_seed_data/"


def test_fetch_api() -> list[dict]:
    test_parcels: list[str] = os.listdir(f"{TEST_UPDATE_FILES_PATH}")

    assert len(test_parcels) == 15

    consumed_parcel_data: list[dict] = []

    for parcel in test_parcels:
        parcel_file = open(f"{TEST_UPDATE_FILES_PATH}{parcel}", "r")
        parcel_data: dict = json.load(parcel_file)
        consumed_parcel_data.append(parcel_data)

    assert len(consumed_parcel_data) == 15


if __name__ == "__main__":
    print(test_fetch_api())

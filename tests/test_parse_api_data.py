from hoa_insights_surpriseaz.schemas import Owners


def test_parse_api_data(parse_owner_seed_data):
    parsed_test_owners, parsed_test_rentals = parse_owner_seed_data
    assert len(parsed_test_owners) == 15
    assert len(parsed_test_rentals) == 4
    assert type(parsed_test_owners[0]) is Owners

    assert parsed_test_owners[0].OWNER == "STALZER CHRISTOPHER T"


if __name__ == "__main__":
    print(test_parse_api_data())

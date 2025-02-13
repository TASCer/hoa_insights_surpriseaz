from hoa_insights_surpriseaz.schemas import Owners, Rentals


def test_parse_api_seed(parse_owner_seed_data):
    parsed_test_owners, parsed_test_rentals = parse_owner_seed_data
    assert len(parsed_test_owners) == 15
    assert len(parsed_test_rentals) == 7
    assert type(parsed_test_owners[0]) is Owners
    assert type(parsed_test_rentals[0]) is Rentals


def test_parse_api_update(parse_owner_update_data):
    parsed_test_owners, parsed_test_rentals = parse_owner_update_data
    assert len(parsed_test_owners) == 2
    assert len(parsed_test_rentals) == 0
    assert type(parsed_test_owners[0]) is Owners
    # assert type(parsed_test_rentals[0]) is Rentals


    assert parsed_test_owners[0].OWNER != "STALZER CHRISTOPHER T"




if __name__ == "__main__":
    print(test_parse_api_seed())

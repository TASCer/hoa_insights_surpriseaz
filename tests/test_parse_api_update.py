from hoa_insights_surpriseaz.schemas import Owners, Rentals


def test_parse_api_update(parse_owner_update_data):
    parsed_test_owners, parsed_test_rentals = parse_owner_update_data
    assert len(parsed_test_owners) == 3
    assert len(parsed_test_rentals) == 1
    assert type(parsed_test_owners[0]) is Owners

from hoa_insights_surpriseaz.schemas import Owners, Rentals


def test_parse_api_update(parse_owner_update_data):
    parsed_test_owners, parsed_test_rentals = parse_owner_update_data
    assert len(parsed_test_owners) == 5
    assert type(parsed_test_owners[0]) is Owners

    assert len(parsed_test_rentals) == 2
    assert type(parsed_test_rentals[0]) is Rentals

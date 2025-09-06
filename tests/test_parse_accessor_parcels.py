from hoa_insights_surpriseaz.schemas import Owners, Rentals


def test_parse_psuedo_api_original(parse_original_parcel_data) -> None:
    parsed_test_original_parcels, parsed_test_original_rentals = (
        parse_original_parcel_data
    )
    assert len(parsed_test_original_parcels) == 5
    assert len(parsed_test_original_rentals) == 2
    assert type(parsed_test_original_parcels[0]) is Owners
    assert type(parsed_test_original_rentals[0]) is Rentals
    original_owner_check = [
        x for x in parsed_test_original_parcels if x.APN == "509-11-455"
    ]
    assert original_owner_check[0].OWNER == "STEVENS TODD"
    assert original_owner_check[0].LEGAL_CODE == "3.1 "
    assert original_owner_check[0].DEED_TYPE == "WD"
    assert original_owner_check[0].RENTAL is False

    assert len(parsed_test_original_rentals) == 2


def test_parse_psuedo_api_new(parse_new_parcel_data):
    parsed_test_update_parcels, parsed_test_update_rentals = parse_new_parcel_data
    assert len(parsed_test_update_parcels) == 5
    assert type(parsed_test_update_parcels[0]) is Owners
    assert len(parsed_test_update_rentals) == 2
    assert type(parsed_test_update_rentals[0]) is Rentals

    updated_owners = [x for x in parsed_test_update_parcels if x.APN == "509-11-455"]

    assert updated_owners[0].OWNER == "BUYER NEW A"
    # TODO test dt
    # assert updated_owners[0].SALE_DATE == datetime.date(2025,1,1)
    assert updated_owners[0].SALE_PRICE == 375000

    assert len(parsed_test_update_rentals) == 2

    assert parsed_test_update_rentals[0].OWNER == "RENTAL NEW A"

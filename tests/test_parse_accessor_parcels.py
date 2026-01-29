import datetime
from hoa_insights_surpriseaz.schemas import Owners, Rentals


def test_parse_psuedo_api_original(parse_original_parcel_data) -> None:
    parsed_test_original_parcels, parsed_test_original_rentals = (
        parse_original_parcel_data
    )

    assert len(parsed_test_original_parcels) == 5
    parsed_owner_types = [type(p) is Owners for p in parsed_test_original_parcels] 
    assert all(parsed_owner_types)

    assert len(parsed_test_original_rentals) == 2
    parsed_rental_types = [type(r) is Rentals for r in parsed_test_original_rentals]
    assert all(parsed_rental_types)

    original_owner_check = [
        x for x in parsed_test_original_parcels if x.APN == "509-11-455"
    ]
    assert original_owner_check[0].OWNER == "STEVENS TODD"
    assert original_owner_check[0].LEGAL_CODE == "3.1 "
    assert original_owner_check[0].DEED_TYPE == "WD"
    assert original_owner_check[0].RENTAL is False


def test_parse_psuedo_api_new(parse_new_parcel_data) -> None:
    parsed_test_update_parcels, parsed_test_update_rentals = parse_new_parcel_data
    assert len(parsed_test_update_parcels) == 5
    assert type(parsed_test_update_parcels[0]) is Owners
    assert len(parsed_test_update_rentals) == 1
    assert type(parsed_test_update_rentals[0]) is Rentals

    updated_owners = [o for o in parsed_test_update_parcels if o.APN == "509-11-455"]
    print(updated_owners)
    assert updated_owners[0].OWNER == "BUYER NEW A"
    assert updated_owners[0].SALE_DATE == datetime.datetime(2025, 1, 1, 0, 0)
    assert updated_owners[0].SALE_PRICE == "375000"

    updated_rentals = [r for r in parsed_test_update_rentals if r.APN == "509-11-022"]

    assert updated_rentals[0].OWNER == "HUDSON SFR PROPERTY HOLDINGS II LLC"

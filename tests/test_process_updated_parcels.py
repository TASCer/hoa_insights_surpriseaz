# THIS IS FOR PRE-REPORT PROCESSING
# from hoa_insights_surpriseaz.database import update_local_tables
# from hoa_insights_surpriseaz.my_secrets import test_debian_uri, test_debian_dbname


def test_initial_parcel_data(parse_original_parcel_data) -> list[dict]:
    initial_parcels, initial_rentals = parse_original_parcel_data
    assert len(parse_original_parcel_data) == 2
    assert len(initial_parcels) == 5

    initial_owner_check = [x for x in initial_parcels if x.APN == "509-11-455"]
    assert initial_owner_check[0].OWNER == "STEVENS TODD"
    assert initial_owner_check[0].LEGAL_CODE == "3.1 "
    assert initial_owner_check[0].DEED_TYPE == "WD"
    assert initial_owner_check[0].RENTAL is False

    assert len(initial_rentals) == 2


def test_new_parcel_data(parse_new_parcel_data) -> list[dict]:
    update_owners, update_rentals = parse_new_parcel_data
    assert len(update_owners) == 5

    updated_owners = [x for x in update_owners if x.APN == "509-11-455"]
    
    assert updated_owners[0].OWNER == "BUYER NEW A"
    # assert updated_owners[0].SALE_DATE == datetime.date(2025,1,1)
    assert updated_owners[0].SALE_PRICE == 375000

    assert len(update_rentals) == 2

    # assert update_rentals[0].OWNER == "RENTAL NEW A"

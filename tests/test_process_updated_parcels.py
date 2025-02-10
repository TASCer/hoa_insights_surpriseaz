from sqlalchemy import text

from hoa_insights_surpriseaz import update_parcel_data
from hoa_insights_surpriseaz.my_secrets import test_debian_uri, test_debian_dbname


# TODO issue getting results from query?
def test_process_updates(session):
    sales = session.execute(
        text(f"SELECT * FROM test_hoa_insights_surpriseaz.historical_sales;")
    )

    sales_updated = sales.fetchall()

    # print(sales_result, len(sales_result))
    sales = [s for s in sales_updated]
    print(sales)
    # assert len(sales) >= 1
    # sess.commit(sales)

    # owners = sess.execute(text("SELECT * from historical_owners"))
    # sess.commit(sales)


#     seed_owners, seed_rentals = parse_owner_seed_data
#     assert len(parse_owner_seed_data) == 2
#     assert len(seed_owners) == 15

#     seed_owner_check = [x for x in seed_owners if x.APN == "509-11-455"]

#     assert seed_owner_check[0].OWNER == "STEVENS TODD"

#     assert len(seed_rentals) == 4

#     update_parcel_data.owners(
#         seed_owners, db_name=test_debian_dbname, db_uri=test_debian_uri
#     )
#     update_parcel_data.rentals(seed_rentals, db_name=test_debian_dbname, db_uri=test_debian_uri)

# def test_update_owner_data(session, parse_owner_update_data) -> list[dict]:
#     update_owners, update_rentals = parse_owner_update_data
#     assert len(parse_owner_update_data) == 2

#     updated_owners = [x for x in update_owners if x.APN == "509-11-455"]

#     assert updated_owners[0].OWNER == "BUYER NEW"

#     assert len(update_rentals) == 3

#     update_parcel_data.owners(update_owners, db_name=test_debian_dbname, db_uri=test_debian_uri)
#     update_parcel_data.rentals(update_rentals, db_name=test_debian_dbname, db_uri=test_debian_uri)


if __name__ == "__main__":
    updates = test_process_updates()

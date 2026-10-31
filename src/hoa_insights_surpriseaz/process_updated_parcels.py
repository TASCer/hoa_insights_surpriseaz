import logging
from logging import Logger
from pathlib import Path

from pandas import DataFrame

from hoa_insights_surpriseaz.database import get_updated_parcels, get_ytd_sales
from hoa_insights_surpriseaz.utils.date_parser import logger_date

logger: Logger = logging.getLogger(__name__)

OWNERS_REPORT_COLUMNS: list[str] = [
    "APN",
    "COMMUNITY",
    "OWNER",
    "DEED_DATE",
    "DEED_TYPE",
]
SALES_REPORT_COLUMNS: list[str] = ["APN", "COMMUNITY", "SALE_DATE", "SALE_PRICE"]

PARCEL_CHANGE_REPORT_COLUMNS: list[str] = [
    "APN",
    "COMMUNTY",
    "OWNER_new",
    "old_owner",
    # "new_sale_date",
    # "old_sale_date",
    # "new_sale_price",
    # "old_sale_price",
    "new_deed_date",
    "old_deed_date",
    "new_deed_deed_type",
    "old_deed_deed_type",
    # "legal_code",
]


def insights(
    updated_parcels: Path, finances: Path
) -> tuple[DataFrame, DataFrame, int, int]:
    """
    Function provides insights into parcel changes after API data fetches.

    :param updated_parcels: directory for parcel change output
    :param finances: directory for finance change output
    :return: owner changes, finance changes, owner change count, sale change count
    """
    logger.info("Started: Processing Updated Parcels")
    new_owners, old_owners, new_sales, old_sales = get_updated_parcels.changes()
    old_owners_change_count: int = len(old_owners)
    new_owners_change_count = len(new_owners)
    print(f"{new_owners_change_count=} - {old_owners_change_count=}")
    old_sales_change_count: int = len(old_sales)
    new_sales_change_count = len(new_sales)
    print(f"{new_sales_change_count=} - {old_sales_change_count=}")

    if old_owners_change_count >= 1 or old_sales_change_count >= 1:
        community_avg_sale: DataFrame = get_ytd_sales.get_average_sale_price(
            finances=finances
        )
    else:
        return DataFrame(), DataFrame(), 0, 0

    # TESTING
    old_owners_df = DataFrame(old_owners).set_index("APN")
    new_owners_df = DataFrame(new_owners).set_index("APN")
    owners_merged_df = old_owners_df.merge(
        new_owners_df, on=["APN", "COMMUNITY"], suffixes=("-", "+")
    )
    old_sales_df = DataFrame(old_sales).set_index("APN")
    new_sales_df = DataFrame(new_sales).set_index("APN")
    sales_merged_df = old_sales_df.merge(
        new_sales_df, on=["APN", "COMMUNITY"], suffixes=("-", "+")
    )

    parcel_changes_df = owners_merged_df.merge(
        sales_merged_df,
        how="outer",
        on=["APN", "COMMUNITY"],
        suffixes=("-", "+"),
        sort=True,
    ).sort_index(axis=1, ascending=True)

    parcel_changes_df.to_csv(path_or_buf=f"{updated_parcels / logger_date()}.csv")

    return (
        parcel_changes_df,
        community_avg_sale,
        old_owners_change_count,
        old_sales_change_count,
    )


# PREVIOUSLY I JUST FOCUSED ON OLD OWNERS AND SALES. NOW REPORT SHOWS WHAT CHANGED WHILE KEEPING DB SAME,
# owner_changes: DataFrame = DataFrame(
#     owners_merged,
#     columns=PARCEL_CHANGE_REPORT_COLUMNS,
# ).set_index(["APN"])
# print(parcel_changes)

# PROD
# if old_owners_change_count >= 1 or old_sales_change_count >= 1:
#     community_avg_sale: DataFrame = get_ytd_sales.get_average_sale_price(
#         finances=finances
#     )

#     owner_changes: DataFrame = DataFrame(
#         old_owners,
#         columns=OWNERS_REPORT_COLUMNS,
#     ).set_index(["APN"])

#     sale_changes: DataFrame = DataFrame(
#         old_sales, columns=SALES_REPORT_COLUMNS
#     ).set_index("APN")

#     merged_changes: DataFrame = owner_changes.merge(
#         sale_changes, how="outer", on=["APN", "COMMUNITY"], suffixes=("", "_y")
#     )

#     merged_changes["SALE_PRICE"] = (
#         merged_changes["SALE_PRICE"].astype(float).fillna(0)
#     )

#     merged_changes.drop(
#         merged_changes.filter(regex="_y$").columns, axis=1, inplace=True
#     )
#     merged_changes.to_csv(path_or_buf=f"{updated_parcels / logger_date()}.csv")


# else:
#     return DataFrame(), DataFrame(), 0, 0

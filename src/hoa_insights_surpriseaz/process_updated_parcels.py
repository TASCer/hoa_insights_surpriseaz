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


def insights(
    updated_parcels: Path, finances: Path
) -> tuple[DataFrame, DataFrame, int, int]:
    """
    Function provides insights by processing changes between parcel API data fetches.

    :param updated_parcels: directory for parcel change output
    :param finances: directory for finance change output
    :return: owner changes, finance changes, owner change count, sale change count
    """
    old_owners, new_owners, old_sales, new_sales = get_updated_parcels.changes()
    old_owners_change_count: int = len(old_owners)
    old_sales_change_count: int = len(old_sales)
    new_sales_change_count = len(new_sales)
    new_owners_change_count = len(new_owners)



    if old_owners_change_count >= 1 or old_sales_change_count >= 1:
        community_avg_sale: DataFrame = get_ytd_sales.get_average_sale_price(
            finances=finances
        )

        owner_changes: DataFrame = DataFrame(
            old_owners,
            columns=OWNERS_REPORT_COLUMNS,
        ).set_index(["APN"])

        sale_changes: DataFrame = DataFrame(
            old_sales, columns=SALES_REPORT_COLUMNS
        ).set_index("APN")

        merged_changes: DataFrame = owner_changes.merge(
            sale_changes, how="outer", on=["APN", "COMMUNITY"], suffixes=("", "_y")
        )

        merged_changes["SALE_PRICE"] = (
            merged_changes["SALE_PRICE"].astype(float).fillna(0)
        )

        merged_changes.drop(
            merged_changes.filter(regex="_y$").columns, axis=1, inplace=True
        )
        merged_changes.to_csv(path_or_buf=f"{updated_parcels / logger_date()}.csv")

        return (
            merged_changes,
            community_avg_sale,
            old_owners_change_count,
            old_sales_change_count,
        )

    else:
        return DataFrame(), DataFrame(), 0, 0

import logging

from hoa_insights_surpriseaz.database import get_ytd_sales
from logging import Logger
from pandas import DataFrame
from pathlib import Path
from hoa_insights_surpriseaz.utils.date_parser import logger_date
from hoa_insights_surpriseaz.database import get_updated_parcels

logger: Logger = logging.getLogger(__name__)


def insights(
    updated_parcels: Path, finances: Path
) -> tuple[DataFrame, DataFrame, int, int]:
    """
    Function provides insights by processing changes between parcel API data fetches.

    :param updated_parcels: directory for parcel change output
    :param finances: directory for finance change output
    :return: owner changes, finance changes, owner change count, sale change count
    """
    owner_changes, sale_changes = get_updated_parcels.changes()
    owner_change_count: int = len(owner_changes)
    sale_change_count: int = len(sale_changes)

    if owner_change_count >= 1 or sale_change_count >= 1:
        community_avg_sale: DataFrame = get_ytd_sales.get_average_sale_price(
            finances=finances
        )

        owner_changes: DataFrame = DataFrame(
            owner_changes,
            columns=["APN", "COMMUNITY", "OWNER", "DEED_DATE", "DEED_TYPE"],
        ).set_index(["APN"])

        sale_changes: DataFrame = DataFrame(
            sale_changes, columns=["APN", "COMMUNITY", "SALE_DATE", "SALE_PRICE"]
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
        merged_changes.to_csv(f"{updated_parcels / logger_date()}.csv")

        return merged_changes, community_avg_sale, owner_change_count, sale_change_count

    else:
        return DataFrame(), DataFrame(), 0, 0

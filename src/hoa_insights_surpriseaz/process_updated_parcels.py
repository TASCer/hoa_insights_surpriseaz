import logging

from hoa_insights_surpriseaz.database import get_ytd_sales
from logging import Logger
from pandas import DataFrame
from pathlib import Path
from hoa_insights_surpriseaz.utils.date_parser import logger_date
from hoa_insights_surpriseaz.database import get_updated_data

logger: Logger = logging.getLogger(__name__)


def insights(
    updated_parcels: Path, finances: Path
) -> tuple[DataFrame, DataFrame, int, int]:
    """
    Function takes in paths to parcel and finanxial change files
    Queries historical_sales and historical_owners tables for items with a timestamp of today.
    Creates a merged dataframe of changes that outputs to csv.
    Returns dataframes.
    """
    owner_changes, sale_changes = get_updated_data.changes()
    owner_change_count: int = len(owner_changes)
    sale_change_count: int = len(sale_changes)

    if sale_change_count >= 1:
        community_avg_sale: DataFrame = get_ytd_sales.get_average_sale_price(
            finances=finances
        )

    if owner_change_count >= 1 or sale_change_count >= 1:
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

        # TODO FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version.
        # TODO Call result.infer_objects(copy=False) instead.
        merged_changes["SALE_PRICE"] = (
            merged_changes["SALE_PRICE"].fillna(0.0).astype(int)
        )

        merged_changes.drop(
            merged_changes.filter(regex="_y$").columns, axis=1, inplace=True
        )
        merged_changes.to_csv(f"{updated_parcels / logger_date()}.csv")

        return merged_changes, community_avg_sale, owner_change_count, sale_change_count

    else:
        return DataFrame(), DataFrame(), 0, 0

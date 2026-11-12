import logging
from logging import Logger
from pathlib import Path

from pandas import DataFrame

from hoa_insights_surpriseaz.database import get_updated_parcels, get_financials
from hoa_insights_surpriseaz.utils.date_parser import logger_date

logger: Logger = logging.getLogger(__name__)


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
        community_avg_sale: DataFrame = get_financials.average_sale_prices(
            finances=finances
        )
    else:
        return DataFrame(), DataFrame(), 0, 0

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

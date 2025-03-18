import logging
import pandas as pd

from hoa_insights_surpriseaz.database import get_ytd_sales
from logging import Logger
from pathlib import Path
from hoa_insights_surpriseaz.utils.date_parser import logger_date
from hoa_insights_surpriseaz.database import get_updated_data

logger: Logger = logging.getLogger(__name__)


UPDATED_PARCELS_PATH = Path.cwd() / "output" / "csv" / "latest_changes"


def insights() -> pd.DataFrame:
    """
    Function retrieves changes to parcel data by querying historical_sales and Historical_owners tables with timestamp of today.
    Creates a merged dataframe of changes that outputs to csv.
    Returns dataframe.
    """
    owner_changes, sale_changes = get_updated_data.changes()
    owner_change_count: int = len(owner_changes)
    sale_change_count: int = len(sale_changes)

    if sale_change_count >= 1:
        get_ytd_sales.get_average_sale_price()

    if owner_change_count >= 1 or sale_change_count >= 1:
        logger.info(
            f"New Owners: {len(owner_changes)} - New Sales: {len(sale_changes)}"
        )
        owner_changes = pd.DataFrame(
            owner_changes,
            columns=["APN", "COMMUNITY", "OWNER", "DEED_DATE", "DEED_TYPE"],
        ).set_index(["APN"])

        sale_changes = pd.DataFrame(
            sale_changes, columns=["APN", "COMMUNITY", "SALE_DATE", "SALE_PRICE"]
        ).set_index("APN")

        merged_changes = owner_changes.merge(
            sale_changes, how="outer", on=["APN", "COMMUNITY"], suffixes=("", "_y")
        )

        merged_changes["SALE_PRICE"] = (
            merged_changes["SALE_PRICE"].fillna(0.0).astype(int)
        )

        merged_changes.drop(
            merged_changes.filter(regex="_y$").columns, axis=1, inplace=True
        )
        merged_changes.to_csv(f"{UPDATED_PARCELS_PATH / logger_date()}.csv")

        return merged_changes

    else:
        return pd.DataFrame()


if __name__ == "__main__":
    print(insights())

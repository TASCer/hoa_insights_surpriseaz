import logging

# from numpy import sort
import pandas as pd

from hoa_insights_surpriseaz.financials import get_ytd_sales
from logging import Logger
from hoa_insights_surpriseaz.utils.date_parser import log_date
from hoa_insights_surpriseaz import get_updated_parcels
from hoa_insights_surpriseaz import my_secrets

logger: Logger = logging.getLogger(__name__)


def get_new_insights() -> pd.DataFrame:
    """
    Function retrieves changes to parcel data by querying historical_sales and Historical_owners tables with timestamp of today.
    Creates a merged dataframe of changes that outputs to csv.
    Returns dataframe.
    """
    owner_updates, sale_updates = get_updated_parcels.check()
    owner_update_count: int = len(owner_updates)
    sale_update_count: int = len(sale_updates)

    if sale_update_count >= 1:
        get_ytd_sales.get_average_sale_price()

    if owner_update_count >= 1 or sale_update_count >= 1:
        logger.info(
            f"New Owners: {len(owner_updates)} - New Sales: {len(sale_updates)}"
        )
        owner_changes = pd.DataFrame(
            owner_updates,
            columns=["APN", "COMMUNITY", "OWNER", "DEED_DATE", "DEED_TYPE"],
        ).set_index(["APN"])

        sale_changes = pd.DataFrame(
            sale_updates, columns=["APN", "COMMUNITY", "SALE_DATE", "SALE_PRICE"]
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
        merged_changes.to_csv(f"{my_secrets.csv_changes_path}{log_date()}.csv")

        return merged_changes

    else:
        return pd.DataFrame()


if __name__ == "__main__":
    print(get_new_insights())

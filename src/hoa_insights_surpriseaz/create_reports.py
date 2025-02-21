import logging

import pandas as pd
import pdfkit as pdf

from hoa_insights_surpriseaz import my_secrets
from hoa_insights_surpriseaz import styles
from hoa_insights_surpriseaz.utils.number_formatter import format_price
from hoa_insights_surpriseaz.utils.date_parser import logger_date
from logging import Logger
from pandas import DataFrame
from pandas.io.formats.style import Styler
from hoa_insights_surpriseaz.utils import file_copier

logger: Logger = logging.getLogger(__name__)


def owner_changes(parcel_updates: DataFrame) -> None:
    """
    Function takes in a dataframe of owner and sale changes.
    Produces and saves html report.
    Sends html report to web server.
    """
    parcel_updates["SALE_PRICE"] = (
        parcel_updates["SALE_PRICE"].fillna(0).astype(int).apply(format_price)
    )
    parcel_updates["SALE_DATE"] = parcel_updates["SALE_DATE"].fillna("")

    parcel_updates = parcel_updates.reset_index()

    parcel_updates_caption: str = f"RECENT PARCEL CHANGES <br> Processed: {logger_date()}"

    parcel_updates_style: Styler = (
        parcel_updates.style.set_table_styles(styles.parcel_updates())
        .set_caption(parcel_updates_caption)
        .hide(axis="index")
    )

    parcel_updates_report: str = f"{my_secrets.html_changes_path}recent_changes.html"
    parcel_updates_style.to_html(parcel_updates_report)

    file_copier.copy(parcel_updates_report)

    # TO PDF and email
    pdf.from_file(parcel_updates_report, "./output/pdf/latest_changes.pdf")


def ytd_community_sales(community_avg_prices: DataFrame) -> None:
    """
    Function takes in a dataFrame of the average community home sales price YTD.
    Produces and saves html report.
    Sends html report to web server for display.
    """
    finance_caption: str = f"AVERAGE SALES PRICE (YTD) <br> PROCESSED: {logger_date()}"

    finance_style: Styler = (
        community_avg_prices.style.set_table_styles(styles.finance_updates())
        .set_caption(finance_caption)
        .hide(axis="index")
    )

    finance_report: str = f"{my_secrets.html_finance_path}community_ytd_sales_avg.html"

    finance_style.to_html(finance_report)
    file_copier.copy(finance_report)

    pdf.from_file(finance_report, "./output/pdf/community_ytd_sales_avg.pdf")


if __name__ == "__main__":
    c_df = pd.read_csv("./output/csv/latest_changes/02-03-25.csv")
    owner_changes()(c_df)
    f_df = pd.read_csv("./output/csv/financial/ytd_community_avg_sale_price.csv")
    ytd_community_sales()(f_df)

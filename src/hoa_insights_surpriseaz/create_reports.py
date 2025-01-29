import logging
import os
import pandas as pd
import pdfkit as pdf
import platform
import shutil

from logging import Logger
from pandas import DataFrame
from pandas.io.formats.style import Styler
from hoa_insights_surpriseaz import my_secrets
from hoa_insights_surpriseaz import styles
from hoa_insights_surpriseaz.utils.number_parser import format_price
from hoa_insights_surpriseaz.utils.date_parser import log_date

logger: Logger = logging.getLogger(__name__)


def parcel_changes(parcel_changes: DataFrame) -> None:
    """
    Function takes in a dataframe of owner and sale changes.
    Produces and saves html report.
    Sends html report to web server.
    """
    parcel_changes["SALE_PRICE"] = (
        parcel_changes["SALE_PRICE"].fillna(0).astype(int).apply(format_price)
    )
    parcel_changes["SALE_DATE"] = parcel_changes["SALE_DATE"].fillna("")

    parcel_changes = parcel_changes.reset_index()

    parcel_changes_caption: str = f"RECENT PARCEL CHANGES <br> Processed: {log_date()}"

    parcel_changes_style: Styler = (
        parcel_changes.style.set_table_styles(styles.get_style_changes())
        .set_caption(parcel_changes_caption)
        .hide(axis="index")
    )

    parcel_changes_report: str = f"{my_secrets.html_changes_path}recent_changes.html"
    parcel_changes_style.to_html(parcel_changes_report)

    if parcel_changes_report:
        if not platform.system() == "Windows":
            try:
                os.system(
                    f"cp {parcel_changes_report} {my_secrets.web_server_path_linux_local}"
                )
                logger.info(
                    f"{parcel_changes_report.split('/')[-1]} sent to tascs.test web server"
                )
            except BaseException as e:
                logger.critical(
                    f"{parcel_changes_report} NOT sent to tascs.test web server. {e}"
                )
        else:
            try:
                shutil.copy(parcel_changes_report, my_secrets.web_server_path_windows)

            except (IOError, FileNotFoundError) as e:
                logger.error(e)

        # TO PDF and email
        pdf.from_file(parcel_changes_report, "./output/pdf/latest_changes.pdf")


def financials(community_avg_prices: DataFrame) -> None:
    """
    Function takes in a dataFrame of the average community home sales price YTD.
    Produces and saves html report.
    Sends html report to web server for display.
    """
    finance_caption: str = f"AVERAGE SALES PRICE (YTD) <br> PROCESSED: {log_date()}"

    finance_style: Styler = (
        community_avg_prices.style.set_table_styles(styles.get_style_finance())
        .set_caption(finance_caption)
        .hide(axis="index")
    )

    finance_report: str = f"{my_secrets.html_finance_path}community_ytd_sales_avg.html"

    finance_style.to_html(finance_report)

    if not platform.system() == "Windows":
        try:
            os.system(f"cp {finance_report} {my_secrets.web_server_path_linux_local}")
            logger.info(
                f"{finance_report.split('/')[-1]} sent to tascs.test web server"
            )
        except BaseException as e:
            logger.critical(f"{finance_report} NOT sent to tascs.test web server. {e}")
    else:
        try:
            shutil.copy(finance_report, my_secrets.web_server_path_windows)

        except (IOError, FileNotFoundError) as e:
            logger.error(e)

    pdf.from_file(finance_report, "./output/pdf/community_ytd_sales_avg.pdf")


if __name__ == "__main__":
    c_df = pd.read_csv("./output/csv/latest_changes/01-23-25.csv")
    parcel_changes(c_df)
    f_df = pd.read_csv("./output/csv/financial/ytd_community_avg_sale_price.csv")
    financials(f_df)

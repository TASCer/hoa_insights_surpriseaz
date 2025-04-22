import logging
import pandas as pd
import pdfkit as pdf

from hoa_insights_surpriseaz import styles
from hoa_insights_surpriseaz.utils.number_formatter import format_price
from hoa_insights_surpriseaz.utils import file_copier
from hoa_insights_surpriseaz.utils.date_parser import logger_date
from logging import Logger
from pandas import DataFrame
from pandas.io.formats.style import Styler
from pathlib import Path

logger: Logger = logging.getLogger(__name__)

PDF_REPORT_PATH = Path.cwd() / "output" / "pdf"
HTML_REPORT_PATH_CHANGES = (
    Path.cwd() / "output" / "web_reports" / "latest_changes" / "recent_changes.html"
)
HTML_REPORT_PATH_FINANCIAL = (
    Path.cwd() / "output" / "web_reports" / "financial" / "community_ytd_sales_avg.html"
)


def owner_changes(parcel_updates: DataFrame) -> None:
    """
    Function takes in a dataframe of owner and sale changes.
    Produces and saves html report.
    Sends html report to web server.
    """
    # TESTING ADDING LINK TO LPS MAP IF COMMUNITY LPS
    parcel_updates['OWNER'] = parcel_updates['OWNER'].apply(lambda row: f'<a href="https://hoa.tascs.test/areaMap.php?{row}">{row}</a>')
    # parcel_updates['OWNER'] = parcel_updates['OWNER'].apply(lambda x: parcel_updates.index)

    parcel_updates["SALE_PRICE"] = (
        parcel_updates["SALE_PRICE"].fillna(0).astype(int).apply(format_price)
    )
    parcel_updates["SALE_DATE"] = parcel_updates["SALE_DATE"].fillna("")

    parcel_updates.sort_values("COMMUNITY", inplace=True, ignore_index=False)

    parcel_updates_caption: str = (
        f"RECENT PARCEL CHANGES <br> Processed: {logger_date()}"
    )

    parcel_updates_style: Styler = parcel_updates.style.set_table_styles(
        styles.parcel_updates()
    ).set_caption(parcel_updates_caption)

    parcel_updates_report: str = f"{HTML_REPORT_PATH_CHANGES}"
    parcel_updates_style.to_html(parcel_updates_report)

    file_copier.copy(parcel_updates_report)

    pdf.from_file(
        input=parcel_updates_report, output_path=PDF_REPORT_PATH / "latest_changes.pdf"
    )


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

    finance_report: str = f"{HTML_REPORT_PATH_FINANCIAL}"

    finance_style.to_html(finance_report)
    file_copier.copy(finance_report)

    pdf.from_file(finance_report, PDF_REPORT_PATH / "community_ytd_sales_avg.pdf")


if __name__ == "__main__":
    f_df = pd.read_csv(
        "./output/csv/financial/ytd_community_avg_sale_price.csv", index_col=0
    )
    print(f_df)
    print(ytd_community_sales(f_df))

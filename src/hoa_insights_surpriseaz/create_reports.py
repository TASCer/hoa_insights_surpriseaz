import logging
import pdfkit as pdf

from hoa_insights_surpriseaz import styles
from hoa_insights_surpriseaz.utils.number_formatter import format_price
from hoa_insights_surpriseaz.utils.date_parser import logger_date
from logging import Logger
from pandas import DataFrame
from pandas.io.formats.style import Styler
from pathlib import Path

logger: Logger = logging.getLogger(__name__)


def parcel_changes(
    parcel_updates: DataFrame, html_parcel_changes: Path, pdf_parcel_changes: Path
) -> Path:
    """
    Function takes in a dataframe of owner and sale changes and paths to output directories.
    Produces and saves an html and pdf file.
    Returns tuple of filepaths.
    """

    parcel_updates["COMMUNITY"] = parcel_updates["COMMUNITY"].apply(
        lambda row: f'<a href="https://hoa.tascs.test/lpsMap.php?{row}">{row}</a>'
        if row == "LPS"
        else f'<a href="https://hoa.tascs.test/areaMap.php?{row}">{row}</a>'
    )

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

    parcel_updates_style.to_html(f"{html_parcel_changes / 'recent_changes.html'}")

    pdf.from_file(
        input=f"{html_parcel_changes / 'recent_changes.html'}",
        output_path=pdf_parcel_changes / "recent_changes.pdf",
    )

    return Path(html_parcel_changes / "recent_changes.html")


def ytd_community_sales(community_avg_prices: DataFrame, html_file, pdf_file) -> Path:
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

    finance_style.to_html(f"{html_file / 'community_ytd_sales_avg.html'}")

    pdf.from_file(
        input=f"{html_file / 'community_ytd_sales_avg.html'}",
        output_path=pdf_file / "community_ytd_sales_avg.pdf",
    )

    return Path(html_file / "community_ytd_sales_avg.html")

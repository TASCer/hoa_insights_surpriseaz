# pdfkit alternative python
import logging

from hoa_insights_surpriseaz import styles
from hoa_insights_surpriseaz.utils.number_formatter import format_price
from hoa_insights_surpriseaz.utils.date_parser import logger_date
from logging import Logger
from pandas import DataFrame
from pandas.io.formats.style import Styler
from pathlib import Path
from weasyprint import HTML


logging.getLogger("fontTools").setLevel(logging.WARNING)
logging.getLogger("weasyprint").setLevel(logging.WARNING)


def parcel_changes(
    parcel_updates: DataFrame, html_parcel_changes: Path, pdf_parcel_changes: Path
) -> Path:
    """
    Function creates a parcel change report from recent parcel updates.

    :param parcel_updates: changed parcels
    :param html_parcel_changes: html file location
    :param pdf_parcel_changes: pdf file location

    :return:  html file location
    """
    parcel_updates["COMMUNITY"] = parcel_updates["COMMUNITY"].apply(
        lambda row: (
            f'<a href="https://hoa.tascs.test/lpsMap.php?{row}">{row}</a>'
            if row == "LPS"
            else f'<a href="https://hoa.tascs.test/areaMap.php?{row}">{row}</a>'
        )
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
    # issue with page layout
    HTML(filename=f"{html_parcel_changes / 'recent_changes.html'}").write_pdf(
        pdf_parcel_changes / "recent_changes.pdf"
    )

    return Path(html_parcel_changes / "recent_changes.html")


def ytd_community_sales(
    community_avg_prices: DataFrame, html_file: Path, pdf_file: Path
) -> Path:
    """
    Function creates financial report(s).

    :param community_avg_prices: grouped dataframe
    :param html_file: html file output location
    :param pdf_file: pdf file output location
    :return: community avg sale html file
    """
    finance_caption: str = f"AVERAGE SALES PRICE (YTD) <br> PROCESSED: {logger_date()}"

    finance_style: Styler = (
        community_avg_prices.style.set_table_styles(styles.finance_updates())
        .set_caption(finance_caption)
        .hide(axis="index")
    )

    finance_style.to_html(f"{html_file / 'community_ytd_sales_avg.html'}")

    HTML(filename=f"{html_file}/community_ytd_sales_avg.html").write_pdf(
        pdf_file / "community_ytd_sales_avg.pdf"
    )

    return Path(html_file / "community_ytd_sales_avg.html")

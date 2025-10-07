import logging

from hoa_insights_surpriseaz import fetch_assessor_parcels
from hoa_insights_surpriseaz import create_reports
from hoa_insights_surpriseaz import parse_assessor_parcels
from hoa_insights_surpriseaz import process_updated_parcels
from hoa_insights_surpriseaz import convert_management_data
from hoa_insights_surpriseaz.database import update_community_management
from hoa_insights_surpriseaz.database import update_remote_database
from hoa_insights_surpriseaz.database import update_local_database
from hoa_insights_surpriseaz import fetch_community_management
from hoa_insights_surpriseaz.utils import (
    date_parser,
    delete_files,
    file_renamer,
    file_copier,
    mailer,
)
from logging import Logger, Formatter
from pathlib import Path

PROJECT_ROOT: Path = Path.cwd()
LOG_DATE: str = str(date_parser.logger_date()) + ".log"

CSV_FINANCIAL: Path = Path.cwd() / "output" / "csv" / "financial"
CSV_FINANCIAL.mkdir(parents=True, exist_ok=True)

CSV_UPDATED_PARCELS: Path = Path.cwd() / "output" / "csv" / "parcel_changes"
CSV_UPDATED_PARCELS.mkdir(parents=True, exist_ok=True)

HTML_REPORT_CHANGES: Path = Path.cwd() / "output" / "web_reports" / "parcel_changes"
HTML_REPORT_CHANGES.mkdir(parents=True, exist_ok=True)

HTML_REPORT_FINANCIAL: Path = Path.cwd() / "output" / "web_reports" / "financial"
HTML_REPORT_FINANCIAL.mkdir(parents=True, exist_ok=True)

PDF_REPORT_CHANGES: Path = Path.cwd() / "output" / "pdf" / "parcel_changes"
PDF_REPORT_CHANGES.mkdir(parents=True, exist_ok=True)

PDF_REPORT_FINANCIAL: Path = Path.cwd() / "output" / "pdf" / "financial"
PDF_REPORT_FINANCIAL.mkdir(parents=True, exist_ok=True)

WEB_SERVER_REPORT_PATH_LINUX = Path("/var/www/html/hoa/reports/")
WEB_SERVER_REPORT_PATH_WINDOWS = Path(
    r"\\OPERATIONS\c$\inetpub\wwwroot\TASCSlocal\hoa\reports"
)

DB_SETUP_LOGFILE: Path = Path.cwd() / "database" / "setup" / "__database-setup__.log"

root_logger: Logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

fh = logging.FileHandler(PROJECT_ROOT.parent.parent / LOG_DATE)
fh.setLevel(logging.DEBUG)

formatter: Formatter = logging.Formatter(
    "%(asctime)s - %(filename)s - %(lineno)d - %(levelname)s - %(message)s"
)
fh.setFormatter(formatter)

root_logger.addHandler(fh)

logger: Logger = logging.getLogger(__name__)


def community_management_update() -> Path:
    """
    Function controls the downloading, renaming, and parsing of downloaded HOA management pdf file.

    :return: location of parsed HOA management csv file
    """
    logger.info("\tSTARTED: Monthly HOA Management Update")
    orig_pdf, new_pdf, mgmt_csv = fetch_community_management.download()
    file_renamed: bool = file_renamer.rename(old=orig_pdf, new=new_pdf)

    if file_renamed:
        parsed_csv: Path = convert_management_data.pdf_to_csv(new_pdf, mgmt_csv)
        update_community_management.update(parsed_csv)

        delete_files.delete()

    return mgmt_csv


def main() -> None:
    """
    Function controls the application. 
    """
    logger.info("*** PARCEL PROCESSING STARTED ***")
    consumed_parcel_api_data: list[dict] = fetch_assessor_parcels.parcels_api()
    parsed_owner_data, parsed_rental_data = parse_assessor_parcels.parser(
        consumed_parcel_api_data
    )
    if parsed_owner_data:
        update_local_database.owners(parsed_owner_data)
    if parsed_rental_data:
        update_local_database.rentals(parsed_rental_data)
    else:
        logger.warning("NO REGISTERED RENTAL PROPERTIES FOUND")

    owner_changes, sale_changes, owner_change_count, sale_change_count = (
        process_updated_parcels.insights(CSV_UPDATED_PARCELS, CSV_FINANCIAL)
    )

    if not owner_changes.empty:
        html_report_file: Path = create_reports.parcel_changes(
            owner_changes, HTML_REPORT_CHANGES, PDF_REPORT_CHANGES
        )
        if html_report_file.exists():
            file_copier.to_webserver(to_copy=html_report_file)
        update_remote_database.rental_tables()

    if not sale_changes.empty:
        financial_report_file: Path = create_reports.ytd_community_sales(
            community_avg_prices=sale_changes,
            html_file=HTML_REPORT_FINANCIAL,
            pdf_file=PDF_REPORT_FINANCIAL,
        )
        if financial_report_file.exists():
            file_copier.to_webserver(to_copy=financial_report_file)
        update_remote_database.financial_tables()

    if owner_changes.empty and sale_changes.empty:
        logger.info("NO SALES AND OWNER CHANGES")

    else:
        mailer.send_mail(f"{owner_change_count=} {sale_change_count=}")

    logger.info("*** PARCEL PROCESSING COMPLETED ***")
    logger.info(f"{owner_change_count=} {sale_change_count=}")


if __name__ == "__main__":
    """
    Checks:
     If db-init.py has been ran by looking for log file.
    Checks:
     Is today is the first Tuesday of this month? If so update community management data.
    Runs:
     Controlling application function: main()    
    """
    if not DB_SETUP_LOGFILE.exists():
        logger.error(f"** '{DB_SETUP_LOGFILE}' not found. **")
        logger.info(
            "To initialize database and create file, run 'uv run db-init.py' from database/setup directory."
        )
        print(
            f"ISSUE: {DB_SETUP_LOGFILE.name} not found. See log: {LOG_DATE} for details."
        )
        exit()

    if date_parser.first_tuesday_of_month():
        mgmt_csv: Path = community_management_update()
        update_community_management.update(mgmt_csv)

    main()

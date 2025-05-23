import logging

from logging import Logger, Formatter
from pandas import DataFrame
from pathlib import Path
from hoa_insights_surpriseaz import fetch_assessor_parcels
from hoa_insights_surpriseaz import create_reports
from hoa_insights_surpriseaz import parse_assessor_parcels
from hoa_insights_surpriseaz import process_updated_parcels
from hoa_insights_surpriseaz import convert_management_data
from hoa_insights_surpriseaz.database import update_community_management
from hoa_insights_surpriseaz.database import update_remote_tables
from hoa_insights_surpriseaz.database import update_local_tables
from hoa_insights_surpriseaz import fetch_community_management
from hoa_insights_surpriseaz.utils import (
    date_parser,
    delete_files,
    rename_files,
    mailer,
)

PROJECT_ROOT: Path = Path.cwd()
LOG_DATE: str = str(date_parser.logger_date()) + ".log"

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


def start_community_management_update() -> Path:
    """
    Function downloads, renames, and parses HOA management pdf.
    Deletes management pdf file to ensure latest data.
    """
    logger.info("\tSTARTED: Monthly HOA Management Update")
    orig_pdf, new_pdf, mgmt_csv = fetch_community_management.download()
    file_renamed: bool = rename_files.rename(old=orig_pdf, new=new_pdf)

    if file_renamed:
        parsed_csv: str = convert_management_data.pdf_to_csv(new_pdf, mgmt_csv)
        update_community_management.update(parsed_csv)

        delete_files.delete()

    return mgmt_csv


def process_parcels() -> None:
    """
    Function fetches parcel data via MARICOPA AZ ACCESSOR API.
    Parses fetched parcel data.
    Updates parcel data to local and remote databases.
    """

    logger.info("********** PARCEL PROCESSING STARTED **********")
    consumed_parcel_api_data: tuple[dict] = fetch_assessor_parcels.parcels_api()
    parsed_owner_data, parsed_rental_data = parse_assessor_parcels.parse(
        consumed_parcel_api_data
    )
    update_local_tables.owners(parsed_owner_data)
    update_local_tables.rentals(parsed_rental_data)
    update_remote_tables.all()


def main() -> bool:
    """
    Function controls the application.
    Returns bool if any owner or sale changes.
    """

    process_parcels()
    changes: DataFrame = process_updated_parcels.insights()

    if not changes.empty:
        create_reports.owner_changes(changes)

        return True

    return False


if __name__ == "__main__":
    """
    Checks:
     Is today is the first Tusday of this month? If so update community management data.
    Runs:
     Controlling application function: main()    
    Checks:
     If parcel changes were encountered
     Sends e-mail.
    """

    if date_parser.first_tuesday_of_month():
        mgmt_csv: Path = start_community_management_update()
        update_community_management.update(mgmt_csv)

    changes: bool = main()

    if not changes:
        logger.info("NO SALES OR OWNER CHANGES")

    mailer.send_mail("HOA INSIGHTS PROCESSING COMPLETE")

    logger.info("********** PARCEL PROCESSING COMPLETED **********")

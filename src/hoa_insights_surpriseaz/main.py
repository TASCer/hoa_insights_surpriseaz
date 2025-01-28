import logging

from logging import Logger, Formatter
from pandas import DataFrame
from hoa_insights_surpriseaz import fetch_api_data
from hoa_insights_surpriseaz import create_reports
from hoa_insights_surpriseaz import parse_api_data
from hoa_insights_surpriseaz import process_updated_parcels
from hoa_insights_surpriseaz import update_management
from hoa_insights_surpriseaz import update_rentals_remote
from hoa_insights_surpriseaz import update_parcel_data
from hoa_insights_surpriseaz import fetch_management_pdf
from hoa_insights_surpriseaz import parse_management_pdf
from hoa_insights_surpriseaz.utils import mailer
from hoa_insights_surpriseaz.utils.date_parser import (
    log_date,
    first_tuesday_of_month,
)
from hoa_insights_surpriseaz.utils.delete_files import delete
from hoa_insights_surpriseaz.utils.rename_files import rename_file

root_logger: Logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

fh = logging.FileHandler(f"../{log_date()}.log")
fh.setLevel(logging.DEBUG)

formatter: Formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s"
)
fh.setFormatter(formatter)

root_logger.addHandler(fh)

logger: Logger = logging.getLogger(__name__)


def process_management() -> None:
    """
    Function downloads, renames, and parses HOA management pdf.
    Deletes management pdf file to ensure latest data.
    """
    logger.info("\tMonthly HOA Management Data Update Started")
    fetch_management_pdf.pdf_download()
    file_renamed: bool = rename_file()

    if file_renamed:
        logger.info("Management file renamed")
        parse_management_pdf.convert_pdf()
        update_management.update()

        delete()


def process_parcels() -> None:
    """
    Function fetches parcel data via MARICOPA AZ ACCESSOR API.
    Parses fetched parcel data.
    Updates parcel data to local and remote databases.
    """

    logger.info("********** PARCEL PROCESSING STARTED **********")
    consumed_api_data = fetch_api_data.parcels_api()
    parsed_owner_data, parsed_rental_data = parse_api_data.parse(consumed_api_data)
    update_parcel_data.owners(parsed_owner_data)
    update_parcel_data.rentals(parsed_rental_data)
    # update_rentals_remote.update()


def main() -> None:
    """
    Function controls the application.
    """
    process_parcels()
    parcel_changes: DataFrame = process_updated_parcels.get_new_insights()

    if not parcel_changes.empty:
        create_reports.parcel_changes(parcel_changes)

        return True

    return False


if __name__ == "__main__":
    if int(log_date().split("-")[1]) == first_tuesday_of_month():
        process_management()
        update_management.update()

    changes: bool = main()

    if not changes:
        logger.info("NO SALES OR OWNER CHANGES")

    mailer.send_mail("HOA INSIGHTS PROCESSING COMPLETE")

    logger.info("********** HOA INSIGHT PROCESSING COMPLETED **********")

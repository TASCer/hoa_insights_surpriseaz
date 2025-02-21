import logging

from logging import Logger, Formatter
from pandas import DataFrame
from hoa_insights_surpriseaz import fetch_assessor_data
from hoa_insights_surpriseaz import create_reports
from hoa_insights_surpriseaz import parse_assessor_data
from hoa_insights_surpriseaz import process_updated_data
from hoa_insights_surpriseaz.database import update_community_management_data
from hoa_insights_surpriseaz.database import update_remote_tables
from hoa_insights_surpriseaz.database import update_local_tables
from hoa_insights_surpriseaz import fetch_community_management_data
# from hoa_insights_surpriseaz import process_community_management_data
from hoa_insights_surpriseaz.utils import (
    date_parser,
    delete_files,
    rename_files,
    mailer,
)

root_logger: Logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

fh = logging.FileHandler(f"../{date_parser.logger_date()}.log")
fh.setLevel(logging.DEBUG)

formatter: Formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s"
)
fh.setFormatter(formatter)

root_logger.addHandler(fh)

logger: Logger = logging.getLogger(__name__)


def process_community_management_data() -> None:
    """
    Function downloads, renames, and parses HOA management pdf.
    Deletes management pdf file to ensure latest data.
    """
    logger.info("\tMonthly HOA Management Data Update Started")
    fetch_community_management_data.download()
    file_renamed: bool = rename_files.rename()

    if file_renamed:
        logger.info("Management file renamed")
        process_community_management_data.convert_pdf()
        update_community_management_data.update()

        delete_files.delete()


def process_parcels() -> None:
    """
    Function fetches parcel data via MARICOPA AZ ACCESSOR API.
    Parses fetched parcel data.
    Updates parcel data to local and remote databases.
    """

    logger.info("********** PARCEL PROCESSING STARTED **********")
    consumed_parcel_api_data = fetch_assessor_data.parcels_api()
    parsed_owner_data, parsed_rental_data = parse_assessor_data.parse(
        consumed_parcel_api_data
    )
    update_local_tables.owners(parsed_owner_data)
    update_local_tables.rentals(parsed_rental_data)
    update_remote_tables.all()


def main() -> None:
    """
    Function controls the application.
    """

    process_parcels()
    parcel_changes: DataFrame = process_updated_data.insights()

    if not parcel_changes.empty:
        create_reports.parcels(parcel_changes)

        return True

    return False


if __name__ == "__main__":
    """
    Checks:
     If today is the first Tusday of this month and if so update community management data.
     If parcel changes were encountered
     Sends e-mail.
    """
    if date_parser.first_tuesday_of_month():
        process_community_management_data()
        update_community_management_data.update()

        delete_files.delete()

    changes: bool = main()

    if not changes:
        logger.info("NO SALES OR OWNER CHANGES")

    # mailer.send_mail("HOA INSIGHTS PROCESSING COMPLETE")

    logger.info("********** HOA INSIGHT PROCESSING COMPLETED **********")
